# -*- coding: utf-8 -*-

from lepl.apps.rfc3696 import Email
from decouple import config
import bcrypt


def gen_pw(password, salt=None):
    return (bcrypt.hashpw(password.encode('utf-8'), salt if salt else
            bcrypt.gensalt(config('HASH_COMPLEXITY', default=10, cast=int))))


def check_pw(password, hashed):
    return gen_pw(password, hashed.encode('utf-8')) == hashed.encode('utf-8')


def is_email(email):
    return Email()(email)
