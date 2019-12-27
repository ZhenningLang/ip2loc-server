import argparse

from . import default_config
from .config_manager import DATA_MODE, Configure
from .context import ContextManager
from .util import EasyDict

ACTION = EasyDict(RUNSERVER='runserver', LOADDATA='loaddata', SHOWPATH='showpath')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='ip2loc', description='IPV4 2 Geo Location Server')

    parser.add_argument('--action', help='', default=ACTION.RUNSERVER,
                        choices=[ACTION.RUNSERVER, ACTION.LOADDATA, ACTION.SHOWPATH])
    parser.add_argument('--data-mode', help='Data mode', choices=[DATA_MODE.MEMORY, DATA_MODE.DATABASE])
    parser.add_argument('--config', help=f'Configure file, by default: {default_config.__file__}',
                        default=default_config.__file__)

    logging_arg_group = parser.add_argument_group('Logging', 'Logging related configures')
    logging_arg_group.add_argument('--no-file-log', help='Do not output logs to file',
                                   action='store_const', const=True, default=False)
    logging_arg_group.add_argument('--log-path', help='Log output path', default=None)

    load_data_arg_group = parser.add_argument_group('Data', 'Load data from .csv to database')
    load_data_arg_group.add_argument('--dataver', help='data current version', default=None)
    load_data_arg_group.add_argument('--csv', help='csv file location', default=None)
    load_data_arg_group.add_argument('--zip', help='zip file location', default=None)
    load_data_arg_group.add_argument('--db', default=None,
        help='Database connection url, ref: https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls')  # noqa

    runserver_arg_group = parser.add_argument_group('Server', 'Server related configures')
    runserver_arg_group.add_argument('--ports', help='server port(s), separated by comma')

    return parser.parse_args()


def start(args: argparse.Namespace = None):
    """Construct configure instance and decide action"""
    args = args or parse_args()
    configure = Configure(config_file=args.config)
    configure.data_mode = args.data_mode or configure.data_mode
    configure.dataver = args.csv or configure.dataver
    configure.zip_loc = args.zip or configure.zip_loc
    configure.csv_loc = args.csv or configure.csv_loc
    configure.log_path = args.log_path or configure.log_path
    configure.log_to_file = not args.no_file_log or configure.log_to_file
    args_ports = []
    if args.ports:
        args_ports = [int(item) for item in str(args.ports).split(',')]
    configure.server_ports = args_ports or configure.server_ports

    action = args.action
    assert action in (ACTION.RUNSERVER, ACTION.LOADDATA, ACTION.SHOWPATH)
    if action == ACTION.RUNSERVER:
        context = ContextManager(configure=configure)
    elif action == ACTION.LOADDATA:
        context = ContextManager(configure=configure)
    elif action == ACTION.SHOWPATH:
        configure.display()
