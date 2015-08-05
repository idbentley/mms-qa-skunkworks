from requests.auth import HTTPDigestAuth

from python_mms_api.backup import Backup
from python_mms_api.automation import Automation
from python_mms_api.cluster import Cluster
from python_mms_api.host import Host
from python_mms_api.restore import Restore
from python_mms_api.snapshot import Snapshot
import logging

logger = logging.getLogger("qa.api.{}".format(__name__))

class MMSClient(object):

	def __init__(self, base_uri, username, api_key):
		self.base_uri = base_uri
		self.auth = HTTPDigestAuth(username, api_key)

	def get_a_client(self, client_name, clazz):
		if client_name not in dir(self):
			setattr(self, client_name, clazz(self.base_uri, self.auth))
		return getattr(self, client_name)

	def get_automation_client(self):
		return self.get_a_client("automation_client", Automation)

	def get_backup_client(self):
		return self.get_a_client("backup_client", Backup)

	def get_cluster_client(self):
		return self.get_a_client("cluster_client", Cluster)

	def get_host_client(self):
		return self.get_a_client("host_client", Host)

	def get_restore_client(self):
		return self.get_a_client("restore_client", Restore)

	def get_snapshot_client(self):
		return self.get_a_client("snapshot_client", Snapshot)