import time
import logging

from python_mms_api.mms_client import MMSClient
from qa_helpers import *
from private_conf import config

#from mms_test_helpers import run_remote_js
GROUP_ID = "55844fcce4b06adf8b229e26"
RS_ID = "v20150623-integrity"
CLUSTER_ID = "186d79f44d0f39015a727d810c6883a7"


def update_automation_config():
	pass

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
	isdb_client = MongoClient(host=config["mms_backup_db_host", "mms_backup_db_port"])
	# Provision machines, and set up hosts before this
	#update_automation_config()
	while automation_working():
		time.sleep(10)
		print("polling automation")
	# start_backup()
	while is_backup_working():
		time.sleep(10)
		print("polling backup")
	if not was_most_recent_integrity_job_successful(GROUP_ID, RS_ID):
		print("most recent integrity job not successful.")

	if not ensure_job_updates(GROUP_ID, RS_ID):
		print("could not ensure that the job was updated apporpriately")
			logging.info("manual check required.")
	logging.error("whoops, something went wrong.")
	schedule_integrity_job(isdb_client, GROUP_ID, RS_ID)