# -*- coding: utf-8 -*-

"""
Context Preparation
"""

import logging

from .config_manager import default_configure, Configure, DATA_MODE
from .models import MemoryDataModel, SQLMemoryDataModel


def data_model_factory(data_mode: str, db_conn_url: str = None):
    if data_mode == DATA_MODE.MEMOERY:
        return MemoryDataModel()
    elif data_mode == DATA_MODE.DATABASE and db_conn_url:
        return SQLMemoryDataModel(db_conn_url)
    elif data_mode == DATA_MODE.DATABASE and not db_conn_url:
        logging.warning(f'Data mode is "{DATA_MODE.DATABASE}" but no database connection url is provided. '
                        f'Use "{DATA_MODE.MEMOERY}" as a replacement.')
    else:
        logging.warning(f'No data mode is specified! Use "{DATA_MODE.MEMOERY}" as default.')
    return MemoryDataModel()


class ContextManager:

    def __init__(self, configure: Configure = default_configure):
        self.configure = configure
        self.data_model = data_model_factory(self.configure.data_mode)
