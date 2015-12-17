# -*- coding: utf-8 -*-

from jsonado.handlers import CORSHandler
from decouple import config


class CurrentUserMixin(CORSHandler):

    def get_current_user(self):
        return self.get_secure_cookie(
            config('USER_AUTH_COOKIE', default='user', cast=str))
