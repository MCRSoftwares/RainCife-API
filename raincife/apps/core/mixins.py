# -*- coding: utf-8 -*-

from decouple import config


class RaincifeTable(object):
    db = config('DEFAULT_DB', default='raincife', cast=str)
