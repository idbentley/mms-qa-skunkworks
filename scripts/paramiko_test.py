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
import paramiko_helper
from private_conf import config

run_id = random.randint(0,1000)
logger = logging.getLogger("qa")

if __name__ == "__main__":
	log_config.config(logger)
	ssh_client = paramiko_helper.get_client(config["ssh_credentials"]["scp_target"])
	std_channels = ssh_client.exec_command('ls')
	paramiko_helper.print_channels(std_channels)
	
	stdin, stdout, stderr = ssh_client.exec_command('cd restores')
	logger.info("{}, \n{}, \n{}".format(stdin, stdout, stderr))

