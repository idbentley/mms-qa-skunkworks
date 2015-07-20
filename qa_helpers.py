import time

current_milli_time = lambda: int(round(time.time() * 1000))

def is_recent_ms(time, error=10000):
	return time > current_milli_time - error

def was_most_recent_integrity_job_successful(isdb_client, group_id, rs_id):
	get_most_recent_integrity_job(isdb_client, group_id, rs_id)
	recent_job = get_most_recent_integrity_job(isdb_client, group_id, rs_id)
	if not recent_job: return false
	return recent_job["finished"] is not None and recent_job["broken"] == False and recent_job["workingOn"] == False


def corrupt_a_snapshot(isdb_client, snapshot_id):
	query = {"_id": snapshot_id}
	update = {
		"$addToSet": {"fileIds": new ObjectId()}
	}
	isdb_client.snapshots.find(query, update)