# -*- coding: utf-8 -*-

"""
IP2LOC Config File
"""

import logging
import os


_CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]


# ------ Server ------
PORTS = (8080, )


# ------ DATA ------
DATA_MODE = 'memory'  # memory or database
DATA_VERSION = 'March 2019'
RAW_CSV_PATH_NAME = os.path.join(_CURRENT_PATH, 'data/IP2LOCATION-LITE-DB5.CSV')
RAW_ZIP_PATH_NAME = os.path.join(_CURRENT_PATH, 'data/IP2LOCATION-LITE-DB5.CSV.ZIP')
# Find details here: https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
DB_CONN_URL = 'sqlite:///{abs_path}'.format(abs_path=os.path.join(_CURRENT_PATH, 'data/data.db'))


# ------ LOGGING ------
LOG_TO_FILE = False
LOG_LEVEL = logging.DEBUG
LOG_FILE_PATH = os.path.join(_CURRENT_PATH, 'data/logs')
LOG_FORMAT = '%(levelname)s (%(asctime)s) %(filename)s > %(funcName)s > line %(lineno)d: \n\t%(message)s'
