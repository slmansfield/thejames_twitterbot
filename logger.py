# import external python modules
import logging


def create_logger():
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    return logger
