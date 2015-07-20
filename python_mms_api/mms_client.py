from requests.auth import HTTPDigestAuth

from python_mms_api.backup import Backup
from python_mms_api.automation import Automation

class MMSClient(object):

	def __init__(self, base_uri, username, api_key):
		self.base_uri = base_uri
		self.auth = HTTPDigestAuth(username, api_key)

	def get_automation_client(self):
		if "automation_client" not in dir(self):
			self.automation_client = Automation(self.base_uri, self.auth)
		return self.automation_client

	def get_backup_client(self):
		if "backup_client" not in dir(self):
			self.backup_client = Backup(self.base_uri, self.auth)
		return self.backup_client

