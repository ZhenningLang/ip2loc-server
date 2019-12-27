import os
import sys

sys.path.insert(0, os.path.join(
    os.path.split(os.path.realpath(__file__))[0], '..'
))

from ip2loc_server.cmd_entry import start  # noqa

if __name__ == '__main__':
    sys.argv += ['--action=showpath']
    start()
