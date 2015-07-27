import logging
import coloredlogs

logger = logging.getLogger("foo")

if __name__ == "__main__":
	coloredlogs.install()
	
	logger.debug("foo")
	logger.info("bar")
	logger.warning("baz")
	logger.error("zoo")