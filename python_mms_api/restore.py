from python_mms_api.helpers import accept_json_header

import requests
import json
import logging
import time

logger = logging.getLogger("qa.api.{}".format(__name__))

class Restore(object):

	def __init__(self, base_uri, auth):
		self.base_uri = base_uri
		self.auth = auth

	def create_http_snapshot_restore(self, group_id, cluster_id, snapshot_id):
		uri = "/api/public/v1.0/groups/{group_id}/clusters/{cluster_id}/restoreJobs"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id, cluster_id=cluster_id)
		request_data = {"snapshotId": snapshot_id}
		resp = requests.post(
			full_uri,
			headers=accept_json_header,
			data=json.dumps(request_data),
			auth=self.auth)
		return resp.json()

	def get_restore_job(self, group_id, cluster_id, job_id):
		uri = "/api/public/v1.0/groups/{group_id}/clusters/{cluster_id}/restoreJobs/{job_id}"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id, cluster_id=cluster_id, job_id=job_id)
		resp = requests.get(full_uri, auth=self.auth)
		if resp.status_code == 404:
			return None
		return resp.json()

	def is_job_finished(self, group_id, cluster_id, job_id):
		job = self.get_restore_job(group_id, cluster_id, job_id)
		return job["statusName"] == "FINISHED"