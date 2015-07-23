import time
import logging
import pymongo
import random
import json
import argparse
from bson.objectid import ObjectId

from python_mms_api.mms_client import MMSClient
from job_helpers import *
from automation_helper import *
from snapshot_helpers import *
from private_conf import config

#from mms_test_helpers import run_remote_js

run_id = random.randint(0,1000)

def update_automation_config(hostname, group_id):
	old_config = automation_client.get_config(group_id)
	rs_id = "integrity-" + str(run_id)
	dbpath = "/data/" + str(run_id) + "_1/"
	add_new_rs(old_config, rs_id, dbpath, hostname, 1, run_id)
	automation_client.update_config(group_id, old_config)
	return rs_id

def automation_working(group_id):
	status = automation_client.get_status(group_id)
	goal_version = status.get("goalVersion")
	print(status)
	for process in status["processes"]:
		if process.get("lastGoalVersionAchieved") != goal_version:
			return True
	return False

def start_backup(group_id, cluster_id):
	while True:
		config = backup_client.get_config(group_id, cluster_id)
		if config is not None:
			break;
		print("waiting for backup client to know about replSet")

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
	print ("rsId " + rs_id)
	while automation_working(args.group_id):
		time.sleep(10)
		print("polling automation")
	cluster_id = None
	while True:
		cluster_id = cluster_client.get_cluster_for_replica_set(args.group_id, rs_id)
		if cluster_id is not None:
			break
	print ("clusterId " + str(cluster_id))
	success = start_backup(args.group_id, cluster_id)
	print("backup patched: " + str(success))
	while is_backup_working(args.group_id, cluster_id):
		time.sleep(10)
		print("polling backup")
	if not was_most_recent_integrity_job_successful(isdb_client, args.group_id, rs_id):
		print("most recent integrity job not successful.")

	if not ensure_job_updates(isdb_client, args.group_id, rs_id):
		print("could not ensure that the job was updated apporpriately")
	snapshot = find_a_snapshot(isdb_client, args.group_id, rs_id)
	corrupt_snapshot(isdb_client, snapshot["_id"])
	schedule_integrity_job(isdb_client, args.group_id, rs_id)
