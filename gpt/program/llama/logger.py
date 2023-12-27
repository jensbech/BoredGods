import logging
import sys


def enable():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
    logger = logging.getLogger()
    logger.disabled = False
