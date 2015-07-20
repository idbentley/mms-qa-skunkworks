from python_mms_api.helpers import accept_json_header

import requests
import json

class Backup(object):

	def __init__(self, base_uri, auth):
		self.base_uri = base_uri
		self.auth = auth

	def get_config(self, group_id, cluster_id):
		uri = "/api/public/v1.0/groups/{group_id}/backupConfigs/{cluster_id}"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id, cluster_id=cluster_id)
		resp = requests.get(full_uri, auth=self.auth)
		return resp.json()

	def patch_config(self, group_id, cluster_id, config):
		uri = "/api/public/v1.0/groups/{group_id}/backupConfigs/{cluster_id}"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id, cluster_id=cluster_id)
		resp = requests.patch(
			full_uri,
			headers=[accept_json_header],
			data=config,
			auth=self.auth)
		return resp.status == 202

