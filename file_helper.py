import requests
import hashlib
import tarfile
import os
import logging

logger = logging.getLogger("qa.{}".format(__name__))

def download_file(dir_context, url):
    local_filename = "{}/{}".format(dir_context, url.split('/')[-1])
    # NOTE the stream=True parameter
    response = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

def sha1_for_file(f, block_size=2**20):
    sha1 = hashlib.sha1()
    while True:
        data = f.read(block_size)
        if not data:
            break
        sha1.update(data)
    return sha1.hexdigest()

def check_hash(comparable_sum, filename):
    with open(filename, 'rb') as f:
        calculated_sum = sha1_for_file(f)
    if calculated_sum == comparable_sum:
        logger.info("Hash matched expectations.")
        return True
    else:
        logger.error("Expected sum {}, but got {}".format(comparable_sum, calculated_sum))
        return False

def untar_file(filename, extract_destination):
	filename_prefix = filename.split('.')[0]
	f = tarfile.open(filename)
	f.extractall(extract_destination)
	return filename_prefix
