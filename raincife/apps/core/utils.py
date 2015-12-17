# -*- coding: utf-8 -*-

from lepl.apps.rfc3696 import Email
from decouple import config
import bcrypt


def gen_pw(password, salt=None):
    """
    Função responsável por gerar uma senha nova senha.
    Geralmente utilizado na etapa de cadastro.
    """
    return (bcrypt.hashpw(password.encode('utf-8'), salt if salt else
            bcrypt.gensalt(config('HASH_COMPLEXITY', default=10, cast=int))))


def check_pw(password, hashed):
    """
    Função responsável por comparar a senha dada (e criptografá-la)
    com a senha presente no banco.
    Geralmente utilizado na etapa de login.
    """
    return gen_pw(password, hashed.encode('utf-8')) == hashed.encode('utf-8')


def is_email(email):
    """
    Função auxiliar para simplificar a validação de endereço de email.
    """
    return Email()(email)
