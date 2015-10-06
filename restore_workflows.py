import paramiko_helper
from file_helper import *
from mongo_helper import *
from noise_helper import *
from private_conf import config

import time
import logging
import pymongo
from pymongo.errors import AutoReconnect

logger = logging.getLogger("qa.{}".format(__name__))

class RestoreTester(object):

	restore_id = None
	group_id = None
	cluster_id = None
	is_pit = False
	pit = None
	snapshot_id = None
	storage_engine = None
	dir_context = "restores"

	def __init__(self, restore_client, group_id, cluster_id, options):
		self.group_id = group_id
		self.cluster_id = cluster_id
		self.restore_client = restore_client

		if "point_in_time" in options and options["point_in_time"] is not None:
			self.is_pit = True
			self.pit = options["point_in_time"]
		else:
			self.snapshot_id = options["snapshot_id"]

		if "wired_tiger" in options and options["wired_tiger"]:
			self.storage_engine = "wiredTiger" if options["wired_tiger"] else "mmapv1"


	def request_restore(self):
		pass

	def wait_for_restore(self):
		while True:
			if self.restore_client.is_job_finished(self.group_id, self.cluster_id, self.restore_id):
				break
		time.sleep(10)


	def get_restore(self):
		pass

	def check_hashes(self):
		pass

	def prepare_restore(self):
		pass

	def start_mongod(self):
		pass

	def get_mongo_connection(self):
		pass

	def kill_mongod(self):
		pass

	def assert_contents(self, mongo_client):
		pass

	def issue_kill_command(self, mongo_client):
		pass

	def check_restore_contents(self):
		try:
			with self.get_mongo_connection() as client:
				self.assert_contents(client)
				self.issue_kill_command(client)
		except AutoReconnect as e:
			pass
		finally:
			self.kill_mongod()

	def clean_up(self):
		pass

	def run(self):
		results = self.request_restore()
		restore_job_doc = results["results"][0]
		self.restore_id = restore_job_doc["id"]
		self.wait_for_restore()
		self.get_restore()
		self.check_hashes()
		self.prepare_restore()
		self.start_mongod()
		self.check_restore_contents()
		self.clean_up()

class LocalPullRestoreTester(RestoreTester):

	saved_file = None
	p = None
	untarred_path = None

	def request_restore(self):
		if self.is_pit:
			restore_job = self.restore_client.create_http_pit_restore(self.group_id, self.cluster_id, self.pit)
		else:
			restore_job = self.restore_client.create_http_snapshot_restore(self.group_id, self.cluster_id, self.snapshot_id)
		return restore_job

	def get_restore(self):
		restore_job = self.restore_client.get_restore_job(self.group_id, self.cluster_id, self.restore_id)
		pull_restore_url = restore_job["delivery"]["url"]
		self.saved_file = download_file(self.dir_context, pull_restore_url)

	def check_hashes(self):
		# Need to get the job again now that the hashes are calculated.
		restore_job = self.restore_client.get_restore_job(self.group_id, self.cluster_id, self.restore_id)
		check_hash(restore_job["hashes"][0]["hash"], self.saved_file)

	def prepare_restore(self):
		self.untarred_path = untar_file(self.saved_file, self.dir_context)

	def start_mongod(self):
		self.p = start_mongo_process(self.untarred_path, self.storage_engine, 28001)

	def get_mongo_connection(self):
		head_conn = pymongo.MongoClient(port=28001, connectTimeoutMS=60000)
		return head_conn

	def kill_mongod(self):
		self.p.terminate()

	def issue_kill_command(self, mongo_client):
		admin_db = mongo_client.admin
		admin_db.command("shutdown")

	def assert_contents(self, mongo_client):
		assert_known_values(mongo_client.test.coll)

	def clean_up(self):
		pass

class ScpRestoreTester(RestoreTester):

	scp_details = None
	ssh_client = None
	saved_file = None
	head_path = None
	remote_mongo = None
	is_individual = False

	def __init__(self, restore_client, group_id, cluster_id, scp_details, options):
		super(ScpRestoreTester, self).__init__(restore_client, group_id, cluster_id, options)
		self.scp_details = scp_details
		self.ssh_client = paramiko_helper.get_client(config["ssh_credentials"]["scp_target"])

	def request_restore(self):
		if self.is_pit:
			restore_job = self.restore_client.create_scp_pit_restore(self.group_id, self.cluster_id, self.pit, self.scp_details, self.is_individual)
		else:
			restore_job = self.restore_client.create_scp_snapshot_restore(self.group_id, self.cluster_id, self.snapshot_id, self.scp_details, self.is_individual)
		return restore_job

	def get_restore(self):
		# NO-OP for SCP restores.
		pass

	def check_hashes(self):
		restore_job = self.restore_client.get_restore_job(self.group_id, self.cluster_id, self.restore_id)
		hashes = restore_job["hashes"]
		if not self.is_individual:
			self.saved_file = hashes[0]["fileName"]
		else:
			self.dir_context = "{}/{}".format(self.dir_context, paramiko_helper.get_dir_with_substring(self.ssh_client, self.dir_context, self.restore_id))
			self.head_path = self.dir_context

		for hash_obj in hashes:
			sha1sum = paramiko_helper.sha_file(self.ssh_client, self.dir_context, hash_obj["fileName"])
			if sha1sum != hash_obj["hash"]:
				logger.error("Expected sum {}, but got {}".format(hash_obj["hash"], sha1sum))

	def prepare_restore(self):
		if not self.is_individual:
			paramiko_helper.untar_file(self.ssh_client, self.dir_context, self.saved_file)
			self.head_path = "{}/{}".format(self.dir_context, self.saved_file.partition(".")[0])
		# No-Op for individual restores

	def start_mongod(self):
		self.remote_mongo = paramiko_helper.RemoteMongo(self.ssh_client, self.head_path, storage_engine=self.storage_engine, port=8089)
		self.remote_mongo.start()

	def get_mongo_connection(self):
		try:
			head_conn = pymongo.MongoClient(host=config["ssh_credentials"]["scp_target"]["hostname"], port=8089, connectTimeoutMS=60000)
			return head_conn
		except ServerSelectionTimeoutError as e:
			logger.error("Could not connect to head - {}".format(e))

	def kill_mongod(self):
		self.remote_mongo.kill()

	def issue_kill_command(self, mongo_client):
		pass

	def assert_contents(self, mongo_client):
		count = mongo_client.test.coll.find().count()
		if count != 3:
			logger.error("Wrong number of docs found.")
		logger.info("Found {} docs.  As expected".format(count))
		assert_known_values(mongo_client.test.coll)


	def clean_up(self):
		pass