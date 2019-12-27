from .server import entry
from .ip2loc import ip2loc
from .log import logger

from art import text2art

name = "ip2loc_server"

__all__ = ('entry', 'ip2loc')

art = text2art('IP2LOC', font='epic')
logger.b_info(f'\n{art}')
