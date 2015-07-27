import logging

import log_config
logger = logging.getLogger("qa")

if __name__ == "__main__":
	log_config.config(logger)
	
	logger.debug("foo")
	logger.info("bar")
	logger.warning("baz")
	logger.error("zoo")