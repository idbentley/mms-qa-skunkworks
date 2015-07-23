from python_mms_api.helpers import accept_json_header

import requests
import json

class Host(object):

	def __init__(self, base_uri, auth):
		self.base_uri = base_uri
		self.auth = auth

	def get_all_hosts(group_id):
		uri = "/api/public/v1.0/groups/{group_id}/hosts"
				full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id)
		resp = requests.get(full_uri, auth=self.auth)
		return resp.json()

	def get_host_by_id(group_id, host_id):
		uri = "/api/public/v1.0/groups/{group_id}/hosts/{host_id}"
				full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id, host_id=host_id)
		resp = requests.get(full_uri, auth=self.auth)
		return resp.json()

	def get_host_by_hostname_and_port(group_id, hostname, port):
		uri = "/api/public/v1.0/groups/{group_id}/hosts/{hostname}:{port}"
				full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id, hostname=hostname, port=port)
		resp = requests.get(full_uri, auth=self.auth)
		return resp.json()

	def get_hosts_by_hostname_prefix(group_id, hostname_prefix):
		uri = "/api/public/v1.0/groups/{group_id}/hosts"
				full_uri = self.base_uri + uri
		full_uri = full_uri.format(group_id=group_id)
		resp = requests.get(full_uri, auth=self.auth)
		all_hosts = resp.json()
		filtered_hosts = []
		for host in all_hosts.get("results"):
			if host.get("hostname").startswith(hostname_prefix):
				filtered_hosts.append(host)

		return filtered_hosts
