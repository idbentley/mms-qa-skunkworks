import time
import logging
import pymongo
import random
import json

from python_mms_api.mms_client import MMSClient
from qa_helpers import *
from private_conf import config

#from mms_test_helpers import run_remote_js
GROUP_ID = "55844fcce4b06adf8b229e26"

run_id = random.randint(0,1000)


def update_automation_config(hostname, group_id):
	old_config = automation_client.get_config(group_id)
	rs_id = "integrity-" + str(run_id)
	dbpath = "/data/" + str(run_id) + "_1/"
	new_process = {
		"version": "3.0.4",
		"name": rs_id + "_1",
		"hostname": hostname,
		"authSchemaVersion": 1,
		"processType": "mongod",
		"args2_6": {
			"port": 27017,
			"replSet": rs_id,
			"dbpath": dbpath,
			"logpath": dbpath + "mongodb.log"
		}
		
	}
	old_config["processes"].append(new_process)
	new_rs = {
		"_id": rs_id,
		"members": [
			{
				"host": rs_id + "_1",
				"priority": 1,
				"votes": 1,
				"slaveDelay": 0,
				"hidden": False,
				"arbiterOnly": False
			}
		]
	}
	old_config["replicaSets"].append(new_rs)
	automation_client.update_config(group_id, old_config)
	return rs_id

def automation_working():
	status = automation_client.get_status(GROUP_ID)
	goal_version = status.get("goalVersion")
	for process in status["processes"]:
		if process.get("lastGoalVersionAchieved") != goal_version:
			return True
	return False

def start_backup():
	config = {
		"groupId": GROUP_ID,
		"clusterId": CLUSTER_ID,
		"statusName": "STARTED",
		"syncSource": "PRIMARY"
	}
	success = backup_client.patch_config(GROUP_ID, CLUSTER_ID, config)

def is_backup_working():
	status = backup_client.get_config(GROUP_ID, CLUSTER_ID)
	status_name = status.get("statusName")
	if status_name == "STARTED":
		return False
	return True

def ensure_job_updates(isdb_client, group_id, rs_id):
	backupjobs_db = isdb_client.backupjobs
	implicit_job = backupjobs-db.jobs.find({
		"groupId": ObjectId(group_id),
		"rsId": rs_id
	})
	snapshot = implicit_job.get("snapshot", {})
	caching_enabled = snapshot.get("caching", False)
	last_updated_ms = snapshot.get("lastUpdatedMS", long_time_ago)
	last_integrity_check_ms = snapshot.get("lastIntegrityCheckMS", long_time_ago)
	if is_recent_ms(last_updated_ms) and is_recent_ms(last_integrity_check_ms):
		return caching_enabled
	return False

if __name__ == "__main__":
	mms_client = MMSClient(
		"https://cloud-qa.mongodb.com",
		config['mms_api_username'],
		config['mms_api_key']
		)
	automation_client = mms_client.get_automation_client()
	backup_client = mms_client.get_backup_client()
	isdb_client = pymongo.MongoClient(host=config["mms_backup_db_host"], port=config["mms_backup_db_port"])
	config = automation_client.get_config(GROUP_ID)
	#print(json.dumps(config, indent=4, separators=(',', ': ')))
	# Provision machines, and set up hosts before this
	rsId = update_automation_config("1-0.ianv20150623.558814b1e4b04bb4be29bcdb.mongo.plumbing", GROUP_ID)
	#while automation_working():
	#	time.sleep(10)
	#	print("polling automation")
	# start_backup()
	#while is_backup_working():
	#	time.sleep(10)
	#	print("polling backup")
	#if not was_most_recent_integrity_job_successful(GROUP_ID, rsId):
	#	print("most recent integrity job not successful.")

	#if not ensure_job_updates(GROUP_ID, rsId):
	#	print("could not ensure that the job was updated apporpriately")
	#logging.error("whoops, something went wrong.")
	#schedule_integrity_job(isdb_client, GROUP_ID, rsId)
