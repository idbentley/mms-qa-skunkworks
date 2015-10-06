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
from restore_workflows import *
import paramiko_helper
from private_conf import config

run_id = random.randint(0,1000)
logger = logging.getLogger("qa")


if __name__ == "__main__":
	log_config.config(logger)
	parser = argparse.ArgumentParser(description="Test pull restore job")
	parser.add_argument(dest="group_id", type=ObjectId, help="The group id to utilize")
	parser.add_argument(dest="hostname", type=str, help="The previously provisioned hostname.")
	parser.add_argument("-c", dest="cluster_id", type=ObjectId, help="Cluster to work upon.  If blank, will create one.")
	parser.add_argument("-wt", dest="wired_tiger", action="store_const", const=True, help="Start backup as Wired Tiger.")
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
	wired_tiger = args.wired_tiger

	## SET UP A BACKUP

	if not cluster_id:
		rs_id = add_replica_set_to_group(automation_client, hostname, group_id, run_id)
		logger.info("rsId {}".format(rs_id))
		block_on_automation_finishing(automation_client, group_id)
		cluster_id = get_cluster_id_for_rs(cluster_client, group_id, rs_id)
		logger.info("clusterId {}".format(cluster_id))
	else:
		cluster = cluster_client.get_cluster(group_id, cluster_id)
		if cluster is None:
			logger.error("Could not find cluster with id {}".format(cluster_id))
			exit(1)
		elif cluster["typeName"] == "REPLICA_SET":
			rs_id = cluster["replicaSetName"]
		else:
			logger.error("Cluster restores not yet implemented")
			exit(1)

	host = host_client.get_primary_host_by_group_and_rs_id(group_id, rs_id)
	logger.info("host {}".format(host))
	host_conn = pymongo.MongoClient(host=host["hostname"], port=host["port"])
	upsert_some_known(host_conn.test.coll)

	if wired_tiger:
		start_wired_tiger_backup(backup_client, group_id, cluster_id)
	else:
		start_backup(backup_client, group_id, cluster_id)


	while True:
		snapshot = snapshot_client.find_most_recent_non_pit_snapshot(group_id, cluster_id)
		if snapshot:
			break
		time.sleep(10)
		logger.debug("waiting for first snapshot")

	# now = time.time()
	# logger.info("inserting data for 5 minutes")
	# while True:
	# 	insert_some_noise(host_conn.other.coll)
	# 	time.sleep(0.5)
	# 	if time.time() - now > 5 * 60:
	# 		break
	# point_in_time = time.time()	
	# time.sleep(10)
	# insert_some_noise(host_conn.other.coll)
	# logger.info("done inserting data.  Now waiting a couple minutes to let the sync slices catchup.")
	# time.sleep(60*2)
	# logger.info("done sleeping.  Time for a PIT restore.")

	## TEST SECTION

	options={"snapshot_id": snapshot["id"], "wired_tiger": wired_tiger}
	restore_tester = LocalPullRestoreTester(restore_client, group_id, cluster_id, options)
	restore_tester.run()

	# pit_options={"is_pit": True, "point_in_time": point_in_time, "wired_tiger": wired_tiger}
	# restore_tester = LocalPullRestoreTester(restore_client, group_id, cluster_id, pit_options)
	# restore_tester.run()
	
	# restore_tester = ScpRestoreTester(restore_client, group_id, cluster_id, config["restore_credentials"]["scp_target"], options)
	# restore_tester.run()

	# restore_tester = ScpRestoreTester(restore_client, group_id, cluster_id, config["restore_credentials"]["scp_target"], pit_options)
	# restore_tester.run()

	# options["individual"] = True
	# restore_tester = ScpRestoreTester(restore_client, group_id, cluster_id, config["restore_credentials"]["scp_target"], options)
	# restore_tester.run()

	# pit_options["individual"] = True
	# restore_tester = ScpRestoreTester(restore_client, group_id, cluster_id, config["restore_credentials"]["scp_target"], pit_options)
	# restore_tester.run()
