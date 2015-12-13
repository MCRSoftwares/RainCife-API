# -*- coding: utf-8 -*-

from jsonado.core.exceptions import BaseError


class AuthError(BaseError):
    """
    Exceção com mensagens para tratar erros de autenticação.
    """
    def message_token_is_none(self, *args):
        """
        Exceção é lançada quando a aplicação recebe algum dado via POST
        e o token não é fornecido junto ao dado.
        """
        return u'O token de autenticação não foi fornecido.'

    def message_invalid_token(self, *args):
        """
        Exceção é lançada quando a aplicação recebe algum dado via POST
        e o token não é considerado inválido, após checagem.
        """
        return u'Token de autenticação inválido.'

    def message_user_is_none(self, *args):
        """
        Exceção é lançada quando a aplicação recebe algum dado via POST
        e o usuário não é fornecido junto ao dado.
        """
        return u'O ID do usuário não foi fornecido.'
