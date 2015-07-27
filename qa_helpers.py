import time
from bson.objectid import ObjectId
import logging

from job_helpers import *

logger = logging.getLogger("qa.{}".format(__name__))

current_milli_time = lambda: int(round(time.time() * 1000))
long_time_ago = 1

def is_recent_ms(time, error=60000):
	return time > current_milli_time() - error


