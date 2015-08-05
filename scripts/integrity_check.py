import time
import logging
import pymongo
import random
import json
import argparse
from bson.objectid import ObjectId
import pprint

import log_config
from python_mms_api.mms_client import MMSClient
from isdb.job_helpers import *
from isdb.snapshot_helpers import *
from automation_helper import *
from private_conf import config

run_id = random.randint(0,1000)
logger = logging.getLogger("qa")

def ensure_job_updates(isdb_client, group_id, rs_id, desired_caching):
	backupjobs_db = isdb_client.backupjobs
	implicit_job = backupjobs_db.jobs.find_one({
		"groupId": ObjectId(group_id),
		"rsId": rs_id
	})
	# logger.info(pprint.pformat(implicit_job))
	snapshot = implicit_job.get("snapshot", {})
	blockstore = implicit_job.get("blockstore", {})
	caching_enabled = snapshot.get("caching", False)
	last_updated_ms = snapshot.get("lastUpdatedMS", long_time_ago)
	last_integrity_check_ms = blockstore.get("lastIntegrityCheckMS", long_time_ago)
	if is_recent_ms(last_updated_ms) and is_recent_ms(last_integrity_check_ms):
		return caching_enabled == desired_caching
	return False

if __name__ == "__main__":
	log_config.config(logger)
	parser = argparse.ArgumentParser(description="Test integrity check job")
	parser.add_argument(dest='group_id', type=ObjectId, help="The group id to utilize")
	parser.add_argument(dest='hostname', type=str, help="The previously provisioned hostname.")
	args = parser.parse_args()
	mms_client = MMSClient(
		config['mms_api_base_url'],
		config['mms_api_username'],
		config['mms_api_key']
		)
	automation_client = mms_client.get_automation_client()
	backup_client = mms_client.get_backup_client()
	cluster_client = mms_client.get_cluster_client()
	isdb_client = pymongo.MongoClient(host=config["mms_backup_db_host"], port=config["mms_backup_db_port"])
	# Provision machines, and set up hosts before this
	rs_id = add_replica_set_to_group(automation_client, args.hostname, args.group_id)
	logger.info("rsId " + rs_id)
	block_on_automation_finishing(automation_client, args.group_id)
	cluster_id = get_cluster_id_for_rs(cluster_client, args.group_id, rs_id)
	logger.info("clusterId " + str(cluster_id))
	
	time.sleep(20) # give it a moment for le pings.
	success = start_backup(backup_client, args.group_id, cluster_id)
	if not success:
		logger.error("Failed to start backup.")
	block_on_backup_finishing(backup_client, args.group_id, cluster_id)

	# Blocks waiting for the job to finish
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

	if not confirm_integrity_job_failed(isdb_client, integrity_job_id):
		logger.error("Integrity check didn't fail.")
	if not ensure_job_updates(isdb_client, args.group_id, rs_id, False):
		logger.error("could not ensure that the job was updated appropriately")
	else:
		logger.info("Integrity check on corruped snapshot failed.  ImplicitJob updated appropriately")

	logger.info("Test Completed Successfully! However an additional check is required.")
	logger.info(" - Wait for the next snapshot and make sure it isn't caching by checking the SnapshotJob logs.")
