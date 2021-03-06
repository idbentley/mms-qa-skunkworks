from bson.objectid import ObjectId
import logging

logger = logging.getLogger("qa.{}".format(__name__))

def find_a_snapshot(isdb_client, group_id, rs_id):
	backupjobs_db = isdb_client.backupjobs
	return backupjobs_db.snapshots.find_one({"rsId": rs_id, "groupId": group_id})

def corrupt_snapshot(isdb_client, snapshot_id):
	logger.info("corrupting snapshot {}".format(snapshot_id))
	backupjobs_db = isdb_client.backupjobs
	query = {"_id": snapshot_id}
	update = {
		"$set": {"files.dummy_file.fileId": ObjectId()}
	}
	res = backupjobs_db.snapshots.update_one(query, update)
	logger.info("updated: {}".format(res.modified_count))

