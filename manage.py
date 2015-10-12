# -*- coding: utf-8 -*-

import sys
from raincife.commands import create_tables
from raincife.commands import create_default_users
from raincife.main import listen


class Commands(object):
    attr_args = []

    def __init__(self, *args, **kwargs):
        if len(sys.argv) == 1:
            raise Exception('No command was given')
        arg = sys.argv[1]
        if hasattr(self, arg):
            try:
                if len(sys.argv) > 2:
                    self.attr_args = sys.argv[2:]
                    getattr(self, arg)(*self.attr_args)
                else:
                    getattr(self, arg)()
            except TypeError:
                raise Exception('Invalid args for command: {0}'.format(arg))
        else:
            raise AttributeError('Invalid command: {0}'.format(arg))

    def runserver(self):
        listen()

    def syncdb(self):
        create_tables()
        create_default_users()

commands = Commands()
