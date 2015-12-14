# -*- coding: utf-8 -*-

from jsonado.db import tables
from decouple import config


class RaincifeTable(tables.Table):
    db = config('DEFAULT_DB', default='raincife', cast=str)
