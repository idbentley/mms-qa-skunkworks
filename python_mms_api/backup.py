from python_mms_api.helpers import accept_json_header

import requests
import json
import logging
import time

logger = logging.getLogger("qa.api.{}".format(__name__))

class Backup(object):

	def __init__(self, base_uri, auth):
		self.base_uri = base_uri
		self.auth = auth

	def get_config(self, group_id, cluster_id):
		while True:
			uri = "/api/public/v1.0/groups/{group_id}/backupConfigs/{cluster_id}"
			full_uri = self.base_uri + uri
			full_uri = full_uri.format(group_id=group_id, cluster_id=cluster_id)
			resp = requests.get(full_uri, auth=self.auth)
			if resp.status_code == 404:
				logger.info("could not find cluster, trying again.")
				time.sleep(10)
				continue
			break
		return resp.json()

	def patch_config(self, group_id, cluster_id, config):
		uri = "/api/public/v1.0/groups/{group_id}/backupConfigs/{cluster_id}"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id, cluster_id=cluster_id)
		while True:
			resp = requests.patch(
				full_uri,
				headers=accept_json_header,
				data=json.dumps(config),
				auth=self.auth)
			if resp.status_code == 404:
				logger.info("could not find cluster, trying again.")
			elif resp.status_code != 202:
				logger.info("problem: {}".format(resp.content))
			break
		return resp.status_code == 202

