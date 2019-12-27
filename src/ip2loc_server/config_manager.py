# -*- coding: utf-8 -*-

import importlib.util

from . import default_config as default_config_data
from .log import logger
from .util import EasyDict

DATA_MODE = EasyDict(MEMORY='memory', DATABASE='database')


class Configure:
    """
    default_configure_instance = Configure()
    """

    ATTR_2_ITEM = (
        ('-', '-'),  # separator
        ('server_ports', 'PORTS'),
        ('-', '-'),  # separator
        ('data_mode', 'DATA_MODE'),
        ('dataver', 'DATA_VERSION'),
        ('csv_loc', 'RAW_CSV_PATH_NAME'),
        ('zip_loc', 'RAW_ZIP_PATH_NAME'),
        ('db_conn_url', 'DB_CONN_URL'),
        ('-', '-'),  # separator
        ('log_level', 'LOG_TO_FILE'),
        ('log_format', 'LOG_LEVEL'),
        ('log_to_file', 'LOG_FILE_PATH'),
        ('log_path', 'LOG_FORMAT'),
        ('-', '-'),  # separator
    )

    def __init__(self, config_file=None,
                 server_ports=default_config_data.PORTS,
                 data_mode=default_config_data.DATA_MODE.lower(),
                 dataver=default_config_data.DATA_VERSION,
                 csv_loc=default_config_data.RAW_CSV_PATH_NAME,
                 zip_loc=default_config_data.RAW_ZIP_PATH_NAME,
                 db_conn_url=default_config_data.DB_CONN_URL,
                 log_level=default_config_data.LOG_LEVEL,
                 log_format=default_config_data.LOG_FORMAT,
                 log_to_file=default_config_data.LOG_TO_FILE,
                 log_path=default_config_data.LOG_FILE_PATH):

        self.config_file = config_file

        # server
        self.server_ports = server_ports

        # data
        self.data_mode = data_mode
        self.dataver = dataver
        self.csv_loc = csv_loc
        self.zip_loc = zip_loc
        self.db_conn_url = db_conn_url

        # log
        self.log_level = log_level
        self.log_format = log_format
        self.log_to_file = log_to_file
        self.log_path = log_path

        # for display
        self._max_length = -1
        self.display_str = ""

        self.load_config_from_file()

    def load_config_from_file(self):
        """ Load configs from {config_path_name} to variable 'CONFIG'
        Side effect: revise global variable 'CONFIG'
        """
        if self.config_file is None:
            module = object()  # A dummy object
        else:
            spec = importlib.util.spec_from_file_location('config', self.config_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        for attr, item in Configure.ATTR_2_ITEM:
            if hasattr(self, attr):
                if hasattr(module, item):
                    setattr(self, attr, getattr(module, item))
                attr_len = len(str(getattr(self, attr)))
                if attr_len > self._max_length:
                    self._max_length = attr_len

    def _gen_display_str(self):
        """Generate self.display_str based on configures"""
        assert self._max_length != -1
        display_template = '| {{:<35}} | {{:<{max_length}}} |'.format(max_length=self._max_length // 5 * 5 + 5)
        separator = '-' * len(display_template.format('', ''))
        buffer = []
        for attr, item in Configure.ATTR_2_ITEM:
            if attr == '-':
                buffer.append(separator)
            else:
                buffer.append(display_template.format(item, str(getattr(self, attr))))

    def display(self):
        self._gen_display_str()
        logger.info(self.display_str)


default_configure = Configure()
