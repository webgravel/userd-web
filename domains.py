import re
import graveldb
import gravelrpc
import cmd_util

PATH = '/gravel/system/node'

class Domain(graveldb.Table('domains', PATH)):
    default = dict(owner=None, port=None)

    def setup(self):
        pass
