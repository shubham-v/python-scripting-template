import logging
import config


def init():
    FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
    FILENAME = config.cfg['LOG_PATH'] + '/backfill-slam.log'
    logging.basicConfig(filename=FILENAME, filemode='a', format=FORMAT, level=logging.DEBUG)