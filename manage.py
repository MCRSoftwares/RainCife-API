# -*- coding: utf-8 -*-

from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado import netutil
from tornado import process
from raincife.routers import routers
from decouple import config
from jsonado.core.utils import ClassFinder
from jsonado.core.utils import Commands
from raincife.logs import ServerLog
import rethinkdb as r


class RaincifeCommands(Commands):
    """
    Classe que define os comandos que podem ser executados ao chamar
    'python manage.py <nome_do_comando>' pelo terminal.
    """
    port = config('PORT', default=8888, cast=int)
    host = config('HOST', default='localhost')
    fork_processes = config('FORK_PROCESSES', default=0, cast=int)

    def cmd_debug(self, *args):
        """
        Comando 'debug', responsável por iniciar o servidor de desenvolvimento.
        """
        port = int(args[0]) if args else self.port
        ServerLog.info(code='dev_server_starting', args=[port])
        app = Application(routers, debug=True, autoreload=False)
        app.listen(port)
        r.set_loop_type('tornado')
        ioloop = IOLoop.current()
        ioloop.add_callback(
            callback=ServerLog.info,
            code='server_started',
            args=[self.host, port]
        )
        ioloop.start()

    def cmd_serve(self, *args):
        """
        Comando 'serve', responsável por iniciar o servidor de produção.
        """
        port = int(args[0]) if args else self.port
        ServerLog.info(code='dev_server_starting', args=[port])
        app = Application(routers)
        sockets = netutil.bind_sockets(port)
        process.fork_processes(self.fork_processes)
        server = HTTPServer(app)
        server.add_sockets(sockets)
        r.set_loop_type('tornado')
        ioloop = IOLoop.current()
        ioloop.add_callback(
            callback=ServerLog.info,
            code='server_started',
            args=[self.host, port]
        )
        ioloop.start()

    def cmd_sync(self, *args):
        """
        Comando 'sync', responsável por sincronizar
        a aplicação com o banco de dados.
        """

        # Procura por todas as subclasses de jsonado.db.tables.Table,
        # dentro do caminho/módulo fornecido.
        tables = ClassFinder(
            'jsonado.db.tables', 'Table').find('raincife/apps/')

        db_list = []
        table_list = []
        index_list = []

        # Itera por um generator que possui as tabelas existentes na aplicação.
        for obj in tables:
            # Criando instância do objeto
            obj = obj()
            # Obtendo sua conexão (host e port do servidor do banco)
            c = obj.get_connection()

            # cada 'obj' é uma instância e subclass da classe Table,
            # contendo os atributos 'db', 'table', 'connection' e 'documents'

            # Checa se o banco já existe.
            r.db_list().contains(obj.get_db()).do(
                lambda db_exists: r.branch(
                    db_exists,
                    {'created': 0},
                    # Caso ele não exista,
                    # um novo banco é criado (nome salvo em obj.get_db())
                    # na conexão (obj.get_connection()).
                    r.db_create(obj.get_db())
                )
            ).run(c)
            redb = r.db(obj.get_db())
            # Checa se a tabela já existe
            redb.table_list().contains(obj.get_table()).do(
                lambda table_exists: r.branch(
                    table_exists,
                    {'created': 0},
                    # Caso ela não exista,
                    # uma nova tabela (nome salvo em obj.get_table())
                    # no banco (obj.get_db()) e conexão (obj.get_connection()).
                    redb.table_create(obj.get_table())
                )
            ).run(c)
            retb = redb.table(obj.get_table())
            if hasattr(obj, 'indexes'):
                # Se a tabela possuir indexes.

                # Itera pelo dicionário de indexes
                for i, value in obj.indexes.iteritems():
                    # Checa se o index já existe.
                    retb.index_list().contains(i).do(
                        lambda index_exists: r.branch(
                            index_exists,
                            {'created': 0},
                            # Caso ele não exista,
                            # um novo index é criado
                            # na tabela (obj.get_table()).
                            retb.index_create(i, value)
                            if value else retb.index_create(i)
                        )
                    ).run(c)
                    index_list.append(i)
            db_list.append(obj.get_db())
            table_list.append(obj.get_table())

        # As linhas abaixo servem para checar se o que tem no servidor
        # (bancos, tabelas e indexes) corresponde ao que existe na aplicação.

        redb_list = r.db_list().run(c)
        redb_list.remove('rethinkdb')

        # Caso haja alguma diferença, ela é tratada.
        # Em geral, as iteração abaixo remove qualquer banco, tabela ou index
        # Que não esteja definido na aplicação.

        # Compara os bancos existentes na aplicação
        # com os existentes no servidor
        self._check_if_exists(db_list, redb_list, c, r.db_drop)
        for db in db_list:
            # Compara as tabelas existentes na aplicação
            # com as existentes no banco
            self._check_if_exists(
                table_list, r.db(db).table_list().run(c),
                c, r.db(db).table_drop)
            for table in table_list:
                # Compara os indexes existentes na aplicação
                # com os existentes na tabela
                self._check_if_exists(
                    index_list, r.db(db).table(table).index_list().run(c),
                    c, r.db(db).table(table).index_drop)

    def _check_if_exists(self, value_list, origin_list, c, command):
        """
        Método auxiliar que checa se um valor existe ou não na tabela dada
        e então executa um comando recebido como argumento.
        """
        for val in origin_list:
            if val not in value_list:
                command(val).run(c)
                return False
        return True

RaincifeCommands()
