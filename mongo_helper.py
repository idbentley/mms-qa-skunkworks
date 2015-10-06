import subprocess

def start_mongo_process(head_dir, storage_engine, port):
	p = subprocess.Popen(["mongod", "--dbpath", head_dir, "--port", str(port), "--nojournal", "--storageEngine", storage_engine])
	return p