# -*- coding: utf-8 -*-

from jsonado.core.exceptions import BaseError


class ValidationError(BaseError):
    """
    Exceção com mensagens para tratar erros de validação de dados.
    """
    def message_invalid_field(self, *args):
        """
        Exceção é lançada quando a aplicação recebe algum dado via POST
        cujo campo não está entre os campos válidos.
        """
        return u'Campo inválido fornecido: "{}" com valor "{}".'.format(*args)

    def message_invalid_type_for_field(self, *args):
        """
        Exceção é lançada quando a aplicação recebe algum dado via POST
        cujo campo está no formato inválido.
        """
        return (u'Era esperada um valor do tipo "{}" para o campo "{}" e '
                u'não "{}".'.format(*args))

    def message_invalid_fields_len(self, *args):
        """
        Exceção é lançada quando a aplicação recebe dados via POST
        cuja quantidade de campos não batem com a quantidade pré-definida.
        """
        return (u'Era esperada uma carga de dados com exatamente {} campos, '
                u'não {}.'.format(*args))
