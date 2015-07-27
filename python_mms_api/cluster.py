from python_mms_api.helpers import accept_json_header

import requests
import json
import logging

logger = logging.getLogger("qa.api.{}".format(__name__))

class Cluster(object):

	def __init__(self, base_uri, auth):
		self.base_uri = base_uri
		self.auth = auth

	def get_clusters(self, group_id):
		uri = "/api/public/v1.0/groups/{group_id}/clusters"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id)
		resp = requests.get(full_uri, auth=self.auth)
		return resp.json()

	def get_cluster_for_replica_set(self, group_id, rs_id):
		uri = "/api/public/v1.0/groups/{group_id}/clusters"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id)
		resp = requests.get(full_uri, auth=self.auth)
		clusters = resp.json().get("results", [])
		for cluster in clusters:
			if cluster.get("typeName") == "REPLICA_SET":
				if cluster.get("replicaSetName") == rs_id:
					return cluster.get("id")
		return None
