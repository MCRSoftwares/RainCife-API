# -*- coding: utf-8 -*-

from decouple import config


USER_AUTH_COOKIE = config('USER_AUTH_COOKIE', default='authuser', cast=str)
