import time
from bson.objectid import ObjectId
import logging

from qa_helpers import *

logger = logging.getLogger("qa.{}".format(__name__))

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
		logger.debug("no job found yet ")
	return recent_jobs.next()

def was_most_recent_integrity_job_successful(isdb_client, group_id, rs_id):
	recent_job = get_most_recent_integrity_job(isdb_client, group_id, rs_id)
	if not recent_job: return False
	return not recent_job["finished"] and not recent_job["broken"] and not recent_job["workingOn"]

def schedule_integrity_job(isdb_client, group_id, rs_id):
	last_integrity_check_job = get_most_recent_integrity_job(isdb_client, group_id, rs_id)
	backupjobs_db = isdb_client.backupjobs
	del last_integrity_check_job["_id"]
	last_integrity_check_job["finished"] = False
	res = backupjobs_db.blockstore_jobs.insert_one(last_integrity_check_job)
	return res.inserted_id

def integrity_job_finished(isdb_client, integrity_job_id):
	backupjobs_db = isdb_client.backupjobs
	job = backupjobs_db.blockstore_jobs.find_one({"_id": integrity_job_id})
	return job["finished"]

def confirm_integrity_job_failed(isdb_client, integrity_job_id):
	backupjobs_db = isdb_client.backupjobs
	job = backupjobs_db.blockstore_jobs.find_one({"_id": integrity_job_id})
	return job["finished"] and job["broken"] and not job["workingOn"]
	