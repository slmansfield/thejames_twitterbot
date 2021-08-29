# import external python modules
import logging


def createLogger():
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    return logger
