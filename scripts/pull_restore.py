import time
import logging
import pymongo
import random
import json
import argparse
from bson.objectid import ObjectId
from pymongo.errors import ServerSelectionTimeoutError
import pprint

import log_config
from python_mms_api.mms_client import MMSClient
from isdb.job_helpers import *
from isdb.snapshot_helpers import *
from automation_helper import *
from backup_helper import *
from cluster_helper import *
from noise_helper import *
from file_helper import *
from mongo_helper import *
from private_conf import config

run_id = random.randint(0,1000)
logger = logging.getLogger("qa")

def check_hash(restore_obj, filename):
	with open(filename, 'rb') as f:
		calculated_sum = sha1_for_file(f)
	for h in restore_obj["hashes"]:
		if h["fileName"] == filename:
			comparable_sum = h["hash"]
			break
	if calculated_sum == comparable_sum:
		logger.info("Hash matched expectations.")
		return True
	else:
		logger.error("Expected sum {}, but got {}".format(comparable_sum, calculated_sum))
		return False



if __name__ == "__main__":
	log_config.config(logger)
	parser = argparse.ArgumentParser(description="Test pull restore job")
	parser.add_argument(dest="group_id", type=ObjectId, help="The group id to utilize")
	parser.add_argument(dest="hostname", type=str, help="The previously provisioned hostname.")
	parser.add_argument("-c", dest="cluster_id", type=ObjectId, help="Cluster to work upon.  If blank, will create one.")
	args = parser.parse_args()
	mms_client = MMSClient(
		config['mms_api_base_url'],
		config['mms_api_username'],
		config['mms_api_key']
		)
	automation_client = mms_client.get_automation_client()
	backup_client = mms_client.get_backup_client()
	cluster_client = mms_client.get_cluster_client()
	snapshot_client = mms_client.get_snapshot_client()
	restore_client = mms_client.get_restore_client()
	host_client = mms_client.get_host_client()
	isdb_client = pymongo.MongoClient(host=config["mms_backup_db_host"], port=config["mms_backup_db_port"])
	group_id = args.group_id
	hostname = args.hostname
	cluster_id = args.cluster_id
	if not cluster_id:
		rs_id = add_replica_set_to_group(automation_client, hostname, group_id, run_id)
		logger.info("rsId {}".format(rs_id))
		block_on_automation_finishing(automation_client, group_id)
		cluster_id = get_cluster_id_for_rs(cluster_client, group_id, rs_id)
		logger.info("clusterId {}".format(cluster_id))
	else:
		cluster = cluster_client.get_cluster(group_id, cluster_id)
		if cluster["typeName"] == "REPLICA_SET":
			rs_id = cluster["replicaSetName"]
		else:
			logger.error("Cluster restores not yet implemented")
			exit(1)

	host = host_client.get_primary_host_by_group_and_rs_id(group_id, rs_id)
	logger.info("host {}".format(host))
	host_conn = pymongo.MongoClient(host=host["hostname"], port=host["port"])
	upsert_some_known(host_conn.test.coll)

	start_backup(backup_client, group_id, cluster_id)
	while True:
		snapshot = snapshot_client.find_most_recent_snapshot(group_id, cluster_id)
		if snapshot:
			break
			time.sleep(10)
			logger.debug("waiting for first snapshot")
	logger.info("restoring snapshot {}".format(snapshot["id"]))

	# Basic http pull restore workflow
	restore_details = restore_client.create_http_snapshot_restore(group_id, cluster_id, snapshot["id"])
	restore = restore_details["results"][0]
	while True:
		if restore_client.is_job_finished(group_id, cluster_id, restore["id"]):
			break
	restore_job = restore_client.get_restore_job(group_id, cluster_id, restore["id"])
	pull_restore_url = restore_job["delivery"]["url"]
	saved_file = download_file(pull_restore_url)
	# Need to get the job again now that the hashes are calculated.
	restore_job = restore_client.get_restore_job(group_id, cluster_id, restore["id"])
	check_hash(restore_job, saved_file)
	untarred_path = untar_file(saved_file)
	try:
		p = start_mongo_process(untarred_path, 28001)
		head_conn = pymongo.MongoClient(port=28001, connectTimeoutMS=60000)
		count = head_conn.test.coll.find().count()
		if count != 3:
			logger.error("Wrong number of docs found.")
		assert_known_values(head_conn.test.coll)
	except ServerSelectionTimeoutError as e:
		logger.error("Could not connect to head - {}".format(e))
	finally:
		p.terminate()