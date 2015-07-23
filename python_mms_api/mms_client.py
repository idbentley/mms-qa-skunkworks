from requests.auth import HTTPDigestAuth

from python_mms_api.backup import Backup
from python_mms_api.automation import Automation
from python_mms_api.cluster import Cluster
from python_mms_api.host import Host

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

	def get_cluster_client(self):
		if "cluster_client" not in dir(self):
			self.cluster_client = Cluster(self.base_uri, self.auth)
		return self.cluster_client

	def get_host_client(self):
		if "host_client" not in dir(self):
			self.host_client = Host(self.base_uri, self.auth)
		return self.host_client	