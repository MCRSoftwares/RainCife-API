# -*- coding: utf-8 -*-

from decouple import config
import rethinkdb as r


USER_AUTH_COOKIE = config('USER_AUTH_COOKIE', default='user', cast=str)
TIMEZONE = r.make_timezone(config('TIMEZONE', default='-03:00'))
