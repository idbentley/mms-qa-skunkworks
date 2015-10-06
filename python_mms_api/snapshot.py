from python_mms_api.helpers import accept_json_header

import requests
import json
import logging
import time

logger = logging.getLogger("qa.api.{}".format(__name__))

class Snapshot(object):

	def __init__(self, base_uri, auth):
		self.base_uri = base_uri
		self.auth = auth

	def find_recent_snapshots(self, group_id, cluster_id):
		while True:
			uri = "/api/public/v1.0/groups/{group_id}/clusters/{cluster_id}/snapshots"
			full_uri = self.base_uri + uri
			full_uri = full_uri.format(group_id=group_id, cluster_id=cluster_id)
			resp = requests.get(full_uri, auth=self.auth)
			if resp.status_code == 404:
				logger.info("could not find cluster, trying again.")
				time.sleep(10)
				continue
			break
		return resp.json()

	def find_most_recent_snapshot(self, group_id, cluster_id):
		snapshots = self.find_recent_snapshots(group_id, cluster_id)
		if snapshots["totalCount"] > 0:
			return snapshots["results"][0]
		return None

	def find_most_recent_non_pit_snapshot(self, group_id, cluster_id):
		snapshots = self.find_recent_snapshots(group_id, cluster_id)
		for snapshot in snapshots["results"]:
			if "pointInTimeRestore" in snapshot and snapshot["pointInTimeRestore"] == True:
				continue
			return snapshot
		return None		