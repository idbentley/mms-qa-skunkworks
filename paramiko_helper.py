import paramiko
import logging
import string
import threading

logger = logging.getLogger("qa.{}".format(__name__))

def get_client(ssh_details):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ssh_details["hostname"], username=ssh_details["username"], key_filename=ssh_details["keyFile"])
	return ssh

def print_channels(std_channels):
	(std_in, std_out, std_err) = std_channels

	logger.info("stdin:")
	try:
		for line in std_in.readlines():
			logger.info("::  {}".format(line))
	except OSError:
		pass

	logger.info("stdout:")
	try:
		for line in std_out.readlines():
			logger.info("::  {}".format(line))
	except OSError:
		pass

	logger.info("stderr:")
	try:
		for line in std_err.readlines():
			logger.error("::  {}".format(line))
	except OSError:
		pass

def print_errors(std_channels):
	(std_in, std_out, std_err) = std_channels

	logger.info("stderr:")
	try:
		for line in std_err.readlines():
			logger.error("::  {}".format(line))
	except OSError:
		pass


def do_ls(ssh_client, dir_context):
	std_channels = ssh_client.exec_command("cd {}; ls".format(dir_context))
	print_channels(std_channels)

def sha_file(ssh_client, dir_context, filename):
	stdin, stdout, stderr = ssh_client.exec_command("cd {}; sha1sum {}".format(dir_context, filename))
	for line in stdout.readlines():
		(sha1sum, sha1filename) = line.split()
		if sha1filename == filename:
			return sha1sum

def untar_file(ssh_client, dir_context, filename):
	stdin, stdout, stderr = ssh_client.exec_command("cd {}; tar -xf {}".format(dir_context, filename))
	try:
		line_gen = stderr.readlines()
		if len(line_gen) > 0:
			logger.error("Could not untar file successfully!")
			for line in line_gen:
				logger.error(line)
	except OSError as e:
		logger.info(e)
		pass

def start_mongo(ssh_client, dir_context, port):
	return ssh_client.exec_command("mongod --port {} --dbpath {}".format(port, dir_context))

def killall_mongo(ssh_client):
	ssh_client.exec_command("killall mongod")


class RemoteMongo(threading.Thread):
	def __init__(self, ssh_client, dir_context, port):
		threading.Thread.__init__(self)
		self.ssh_client = ssh_client
		self.dir_context = dir_context
		self.port = port
		self.alive = True

	def kill(self):
		self.alive = False

	def run(self):
		stdin, stdout, stderr = start_mongo(self.ssh_client, self.dir_context, self.port)
		while self.alive:
			stdout.readline()
		killall_mongo(self.ssh_client)
