import subprocess

def start_mongo_process(head_dir, port):
	p = subprocess.Popen(["mongod", "--dbpath", head_dir, "--port", str(port), "--nojournal"])
	return p