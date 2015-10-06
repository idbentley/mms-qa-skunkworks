import time
from bson.objectid import ObjectId
import logging

logger = logging.getLogger("qa.{}".format(__name__))

current_milli_time = lambda: int(round(time.time() * 1000))
long_time_ago = 1

def is_recent_ms(t, error=60000):
	return t > current_milli_time() - error


def how_recent(t):
	return current_milli_time() - t
