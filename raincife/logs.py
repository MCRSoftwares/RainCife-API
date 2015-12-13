# -*- coding: utf-8 -*-


from jsonado.core.utils import Logger


class ServerLog(Logger):
    """
    Classe responsável por tratar os logs do servidor.
    """
    def log_dev_server_starting(self, *args):
        """
        Mensagem exibida quando o servidor de desenvolvimento tenta iniciar.
        """
        return u'Iniciando servidor de desenvolvimento na porta {0}...'.format(
            *args
        )

    def log_prod_server_starting(self, *args):
        """
        Mensagem exibida quando o servidor de produção tenta iniciar.
        """
        return u'Iniciando servidor de produção na porta {0}...'.format(*args)

    def log_server_started(self, *args):
        """
        Mensagem exibida quando o servidor
        (tanto de desenvolvimento quanto de produção) é iniciado.
        """
        return u'Servidor aberto em: http://{0}:{1}/'.format(*args)
