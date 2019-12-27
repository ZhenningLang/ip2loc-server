# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import TimedRotatingFileHandler


__all__ = ('logger', )


class _BufferLogger:
    """
    Not Thread Safe!
    """

    def __init__(self):
        self.logger = None
        self.buffer = []

    # noinspection PyShadowingBuiltins
    def setup(self, log_to_file=False, log_file_loc=None, level=logging.DEBUG, format=None):
        # stream handler (to console)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(format)
        handlers = [stream_handler]

        # file handler
        if log_to_file:
            err = None
            log_path = None
            try:
                if os.path.isdir(log_file_loc):  # convert path to file name
                    log_file_loc = os.path.join(log_file_loc, 'ip2loc.log')

                log_path = os.path.dirname(log_file_loc)
                if not os.path.isdir(log_path):
                    os.makedirs(log_path, exist_ok=True)
            except Exception as e:
                err = e
            finally:
                if log_path is not None and os.path.isdir(log_path):
                    file_handler = TimedRotatingFileHandler(log_file_loc, when='midnight', backupCount=7)
                    file_handler.setFormatter(format)
                    handlers.append(file_handler)

        # set logger
        self.logger = logging.getLogger('IP2LOC')
        self.logger.setLevel(level)
        for handler in handlers:
            self.logger.addHandler(handler)
        if log_to_file and len(handlers) == 1:
            logging.error(f"Cannot create file logger at '{log_file_loc}', error: {err}")

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warn(self, *args, **kwargs):
        self.logger.warn(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)

    def b_debug(self, *args, **kwargs):
        self.buffer.append((self.debug, args, kwargs))

    def b_info(self, *args, **kwargs):
        self.buffer.append((self.info, args, kwargs))

    def b_warn(self, *args, **kwargs):
        self.buffer.append((self.warn, args, kwargs))

    def b_error(self, *args, **kwargs):
        self.buffer.append((self.error, args, kwargs))

    def b_critical(self, *args, **kwargs):
        self.buffer.append((self.critical, args, kwargs))

    def flush_buffer(self):
        for method, args, kwargs in self.buffer:
            method(*args, **kwargs)


_BufferLogger.fatal = _BufferLogger.critical
_BufferLogger.warning = _BufferLogger.warn
_BufferLogger.b_fatal = _BufferLogger.b_critical
_BufferLogger.b_warning = _BufferLogger.b_warn


logger = _BufferLogger()
