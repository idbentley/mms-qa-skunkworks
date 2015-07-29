import logging
import random
import argparse
from bson.objectid import ObjectId
import pprint
import time

from python_mms_api.mms_client import MMSClient
from automation_helper import *
import log_config
from private_conf import config

run_id = random.randint(0,1000)

logger = logging.getLogger("qa.scripts.cluster_test")
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
	log_config.config(logger)
	parser = argparse.ArgumentParser(description="Test lib for createing cluster configs.")
	parser.add_argument(dest='group_id', type=ObjectId, help="The group id to utilize")
	parser.add_argument(dest='hostname', type=str, help="The previously provisioned hostname.")
	args = parser.parse_args()

	mms_client = MMSClient(
		config['mms_api_base_url'],
		config['mms_api_username'],
		config['mms_api_key']
	)
	automation_client = mms_client.get_automation_client()

	old_config = automation_client.get_config(args.group_id)
	add_new_cluster(old_config, "cluster_test", args.hostname, 3, 3, run_id)
	# logger.info(pprint.pformat(old_config))
	automation_client.update_config(args.group_id, old_config)
	while automation_client.automation_working(args.group_id):
		time.sleep(10)
		logger.debug("polling automation")