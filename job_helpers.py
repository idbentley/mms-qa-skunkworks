

def get_most_recent_integrity_job(isdb_client, group_id, rs_id):
	backupjobs_db = isdb_client.backupjobs
	recent_job = backupjobs_db.blockstore_jobs.find({
		"type": "integrityCheck",
		"groupId": ObjectId(group_id),
		"rsId": rs_id,
	}).sort({'finished': -1}).limit(1)[0]
	return recent_job

def schedule_integrity_job(isdb_client, group_id, rs_id):
	last_integrity_check_job = get_most_recent_integrity_job(isdb_client, group_id, rs_id)
	backupjobs_db = isdb_client.backupjobs
	del last_integrity_check_job["_id"]
	last_integrity_check_job.put("finished", False)
	backupjobs_db.blockstore_jobs.insert(last_integrity_check_job)