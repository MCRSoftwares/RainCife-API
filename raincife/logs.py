# -*- coding: utf-8 -*-


from jsonado.core.utils import Logger


class ServerLog(Logger):

    def log_dev_server_starting(self, *args):
        return u'Iniciando servidor de desenvolvimento na porta {0}...'.format(
            *args
        )

    def log_prod_server_starting(self, *args):
        return u'Iniciando servidor de produção na porta {0}...'.format(*args)

    def log_server_started(self, *args):
        return u'Servidor aberto em: http://{0}:{1}/'.format(*args)
