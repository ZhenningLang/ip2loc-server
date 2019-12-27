# -*- coding: utf-8 -*-

import logging
from multiprocessing import Process
import os
import socket
import sqlite3
from urllib.parse import urlparse

import tornado.ioloop
import tornado.web

# from .config_manager import load_config, display_path, CONFIG
from .cmd_entry import start, parse_args
from .data import check_data_version, load_data
# from log import setup_logger
from .ip2loc import ip2loc


db_conn = None
CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]


def init_db_conn(sqlite_path_name):
    global db_conn
    db_conn = sqlite3.connect(sqlite_path_name)


# noinspection PyAbstractClass
class IP2LOCHandler(tornado.web.RequestHandler):

    def get(self):
        ip = self.get_argument('ip')
        # noinspection PyTypeChecker
        self.write(ip2loc(conn=db_conn, ip=ip))


# noinspection PyAbstractClass
class Url2LOCHandler(tornado.web.RequestHandler):

    def get(self):
        url = self.get_argument('url')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = f'http://{url}'
        netloc = urlparse(url).netloc
        ip = socket.gethostbyname(netloc)
        # noinspection PyTypeChecker
        self.write(ip2loc(conn=db_conn, ip=ip))


def start_tornado_server(port):
    app = tornado.web.Application([
        (r"/ip2loc", IP2LOCHandler),
        (r"/url2loc", Url2LOCHandler),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": os.path.join(CURRENT_PATH, 'data')}),
    ])
    app.listen(port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, InterruptedError):
        logging.info(f'User interrupt server on port {port}')


def runserver(sqlite_path_name, ports):
    init_db_conn(sqlite_path_name)

    assert len(ports) > 0
    if len(ports) == 1:
        logging.info(f'Starting local server on port {ports[0]}')
    else:
        logging.info(f'Starting local server on ports {ports}')

    for port in ports:
        # noinspection PyBroadException
        try:
            Process(
                target=start_tornado_server, kwargs={'port': port}).start()
            logging.info(f"\n>>>>> Start ip2loc server on port {port} success! <<<<<\n")
        except Exception as e:
            logging.error(f"Start ip2loc server on port {port} fail with error: {e}", exc_info=True)


def entry():
    args = parse_args()
    load_config(config_path_name=args.config)
    setup_logger()
    display_path(args)
    if args.showpath and not args.loaddata and not args.runserver:
        # only showpath
        exit(0)
    adjust_arguments(args)

    if args.loaddata:
        csv_path_name = args.csv or CONFIG.PATH.RAW_CSV_PATH_NAME
        zip_path_name = args.zip or CONFIG.PATH.RAW_ZIP_PATH_NAME
        unzip = False
        if csv_path_name and os.path.exists(csv_path_name) and os.path.getsize(csv_path_name) > 0:
            # csv file is available
            logging.info(f"Load data: \n"
                         f"\tfrom '{csv_path_name}' \n"
                         f"\tto '{CONFIG.PATH.SQLITE_DATA_PATH_NAME}' \n"
                         f"\tdata version: {args.dataver if args.dataver else 'Not specified'}")
        elif zip_path_name and os.path.exists(zip_path_name) and os.path.getsize(zip_path_name) > 0:
            # csv file is not available but zip file is
            logging.info(f"Load data: \n"
                         f"\tfrom '{zip_path_name}' \n"
                         f"\tto '{CONFIG.PATH.SQLITE_DATA_PATH_NAME}' \n"
                         f"\tdata version: {args.dataver if args.dataver else 'Not specified'}")
            unzip = True
        else:
            logging.fatal('Neither CSV nor ZIP file is available for data loading.')
            logging.info("See 'Track the Latest Data' in README for where to download the data and how to load.")
            exit(1)

        load_data(
            csv_path_name=csv_path_name, zip_path_name=zip_path_name, unzip=unzip,
            sqlite_path_name=CONFIG.PATH.SQLITE_DATA_PATH_NAME, specified_version=args.dataver)

    if args.runserver:
        check_data_version()
        runserver(sqlite_path_name=CONFIG.PATH.SQLITE_DATA_PATH_NAME, ports=CONFIG.SERVER.PORTS)