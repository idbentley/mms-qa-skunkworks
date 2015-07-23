import time
from bson.objectid import ObjectId

from qa_helpers import *

def get_most_recent_integrity_job(isdb_client, group_id, rs_id):
	backupjobs_db = isdb_client.backupjobs
	while True:
		recent_jobs = backupjobs_db.blockstore_jobs.find({
			"type": "integrityCheck",
			"groupId": group_id,
			"rsId": rs_id,
		}).sort('finished', -1)
		if recent_jobs.count() > 0:
			break
		time.sleep(10)
		print("no job found yet ")
	return recent_jobs.next()

def was_most_recent_integrity_job_successful(isdb_client, group_id, rs_id):
	recent_job = get_most_recent_integrity_job(isdb_client, group_id, rs_id)
	print(recent_job)
	if not recent_job: return False
	return recent_job["finished"] is not None and recent_job["broken"] == False and recent_job["workingOn"] == False

def schedule_integrity_job(isdb_client, group_id, rs_id):
	last_integrity_check_job = get_most_recent_integrity_job(isdb_client, group_id, rs_id)
	backupjobs_db = isdb_client.backupjobs
	del last_integrity_check_job["_id"]
	last_integrity_check_job["finished"] = False
	backupjobs_db.blockstore_jobs.insert(last_integrity_check_job)

def ensure_job_updates(isdb_client, group_id, rs_id):
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
		return caching_enabled
	return False
