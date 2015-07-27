import logging
from colorlog import ColoredFormatter

formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s [%(name)s-%(lineno)d]@%(asctime)s:%(reset)s %(white)s%(message)s%(reset)s",
        datefmt=None,
        reset=True,
        log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
)

def config(logger):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(ch)