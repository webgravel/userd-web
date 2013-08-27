import re
import graveldb
import gravelrpc
import cmd_util

PATH = '/gravel/system/nodecache'

class Domain(graveldb.Table('domains', PATH)):
    default = dict(owner=None, port=None, forward=None)

    def setup(self):
        pass
