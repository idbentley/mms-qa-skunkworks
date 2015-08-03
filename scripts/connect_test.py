import time
import logging
import pymongo
import random
import json
import argparse
from bson.objectid import ObjectId
import pprint

import log_config
from python_mms_api.mms_client import MMSClient
from isdb.job_helpers import *
from isdb.snapshot_helpers import *
from private_conf import config

logger = logging.getLogger("qa")

if __name__ == "__main__":
	log_config.config(logger)
	parser = argparse.ArgumentParser(description="Test integrity check job")
	parser.add_argument(dest='group_id', type=ObjectId, help="The group id to utilize")
	parser.add_argument(dest='rs_id', type=str, help="The existing rsId.")
	args = parser.parse_args()
	mms_client = MMSClient(
		config['mms_api_base_url'],
		config['mms_api_username'],
		config['mms_api_key']
		)
	host_client = mms_client.get_host_client()
	# while True:
	# 	cluster_id = cluster_client.get_cluster_for_replica_set(args.group_id, args.rs_id)
	# 	if cluster_id is not None:
	# 		break
	# logger.info("clusterId " + str(cluster_id))
	host = host_client.get_primary_host_by_group_and_rs_id(args.group_id, args.rs_id)
	logger.info("host {}".format(host))
	host_conn = pymongo.MongoClient(host=host["hostname"], port=host["port"])
	host_conn.foo.bar.insert({})