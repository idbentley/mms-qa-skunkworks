import time
import logging
import pymongo
import random
import json
import argparse
from bson.objectid import ObjectId
import coloredlogs

from python_mms_api.mms_client import MMSClient
from job_helpers import *
from automation_helper import *
from snapshot_helpers import *
from private_conf import config

run_id = random.randint(0,1000)
logger = logging.getLogger("scripts.{}".format(__name__))

def ensure_job_updates(isdb_client, group_id, rs_id, desired_caching):
	backupjobs_db = isdb_client.backupjobs
	implicit_job = backupjobs_db.jobs.find_one({
		"groupId": ObjectId(group_id),
		"rsId": rs_id
	})
	snapshot = implicit_job.get("snapshot", {})
	blockstore = implicit_job.get("blockstore", {})
	caching_enabled = snapshot.get("caching", False)
	last_updated_ms = snapshot.get("lastUpdatedMS", long_time_ago)
	last_integrity_check_ms = blockstore.get("lastIntegrityCheckMS", long_time_ago)
	if is_recent_ms(last_updated_ms) and is_recent_ms(last_integrity_check_ms):
		return caching_enabled == desired_caching
	return False


def update_automation_config(hostname, group_id):
	old_config = automation_client.get_config(group_id)
	rs_id = "integrity-" + str(run_id)
	dbpath = "/data/" + str(run_id) + "_1/"
	add_new_rs(old_config, rs_id, dbpath, hostname, 1, run_id)
	automation_client.update_config(group_id, old_config)
	return rs_id


def start_backup(group_id, cluster_id):
	while True:
		config = backup_client.get_config(group_id, cluster_id)
		if config is not None:
			break;
		logger.debug("waiting for backup client to know about replSet")

	config = {
		"groupId": str(group_id),
		"clusterId": cluster_id,
		"statusName": "STARTED",
		"syncSource": "PRIMARY"
	}
	return backup_client.patch_config(group_id, cluster_id, config)

def is_backup_working(group_id, cluster_id):
	status = backup_client.get_config(group_id, cluster_id)
	status_name = status.get("statusName")
	if status_name == "STARTED":
		return False
	return True

if __name__ == "__main__":
	coloredlogs.install()
	parser = argparse.ArgumentParser(description="Test integrity check job")
	parser.add_argument(dest='group_id', type=ObjectId, help="The group id to utilize")
	parser.add_argument(dest='hostname', type=str, help="The previously provisioned hostname.")
	args = parser.parse_args()
	mms_client = MMSClient(
		"https://cloud-qa.mongodb.com",
		config['mms_api_username'],
		config['mms_api_key']
		)
	automation_client = mms_client.get_automation_client()
	backup_client = mms_client.get_backup_client()
	cluster_client = mms_client.get_cluster_client()
	isdb_client = pymongo.MongoClient(host=config["mms_backup_db_host"], port=config["mms_backup_db_port"])
	# Provision machines, and set up hosts before this
	rs_id = update_automation_config(args.hostname, args.group_id)
	logger.info("rsId " + rs_id)
	while automation_client.automation_working(args.group_id):
		time.sleep(10)
		logger.debug("polling automation")
	cluster_id = None
	while True:
		cluster_id = cluster_client.get_cluster_for_replica_set(args.group_id, rs_id)
		if cluster_id is not None:
			break
	logger.info("clusterId " + str(cluster_id))
	success = start_backup(args.group_id, cluster_id)
	logger.debug("backup patched: " + str(success))
	while is_backup_working(args.group_id, cluster_id):
		time.sleep(10)
		logger.debug("polling backup")

	while find_a_snapshot(isdb_client, args.group_id, rs_id) is None:
		time.sleep(10)
		logger.debug("waiting for first snapshot")
	
	if not was_most_recent_integrity_job_successful(isdb_client, args.group_id, rs_id):
		logger.debug("most recent integrity job not successful.")
	
	if not ensure_job_updates(isdb_client, args.group_id, rs_id, True):
		logger.error("could not ensure that the job was updated apropriately")
	snapshot = find_a_snapshot(isdb_client, args.group_id, rs_id)
	if snapshot is None or "_id" not in snapshot:
		logger.error("could not find usable snapshot.")
	corrupt_snapshot(isdb_client, snapshot["_id"])
	integrity_job_id = schedule_integrity_job(isdb_client, args.group_id, rs_id)
	while not integrity_job_finished(isdb_client, integrity_job_id):
		time.sleep(10)
		logger.debug("waiting on integrity job")
	confirm_integrity_job_failed(isdb_client, integrity_job_id)
	ensure_job_updates(isdb_client, args.group_id, rs_id, False)