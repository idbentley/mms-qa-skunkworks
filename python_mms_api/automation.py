#from mms_client.automation_config import AutomationConfig
from python_mms_api.helpers import accept_json_header

import requests
import json

class Automation(object):

	def __init__(self, base_uri, auth):
		self.base_uri = base_uri
		self.auth = auth

	def get_config(self, group_id):
		uri = "/api/public/v1.0/groups/{group_id}/automationConfig"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id)
		resp = requests.get(full_uri, auth=self.auth)
		#return AutomationConfig.parse_json(resp.json())
		return resp.json()

	def update_config(self, group_id, config):
		uri = "/api/public/v1.0/groups/{group_id}/automationConfig"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id)
		resp = requests.put(
			full_uri,
			headers=accept_json_header,
			auth=self.auth,
			data=json.dumps(config))
		return resp.status_code == 200

	def get_status(self, group_id):
		uri = "/api/public/v1.0/groups/{group_id}/automationStatus"
		full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id)
		resp = requests.get(full_uri, auth=self.auth)
		return resp.json()

	def automation_working(self, group_id):
		status = automation_client.get_status(group_id)
		goal_version = status.get("goalVersion")
		print(status)
		for process in status["processes"]:
			if process.get("lastGoalVersionAchieved") != goal_version:
				return True
		return False
