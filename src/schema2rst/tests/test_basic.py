# -*- coding: utf-8 -*-

import io
import os
import unittest
import tempfile
import sqlalchemy
import testing.mysqld

from schema2rst.commands import graph, rst


class TestSchema2rst(unittest.TestCase):
    def setUp(self):
        self.mysqld = testing.mysqld.Mysqld(my_cnf={'skip-networking': None})

        param = self.mysqld.dsn()
        self.config = tempfile.NamedTemporaryFile('w+')
        self.config.write("db: %s\nuser: %s\npasswd: \"\"\nunix_socket: %s\n" %
                          (param['db'], param['user'], param['unix_socket']))
        self.config.flush()

        # switch default dialect to pymysql
        from sqlalchemy.dialects.mysql import base, pymysql
        self.default_dialect = base.dialect
        base.dialect = pymysql.dialect

    def tearDown(self):
        # write back default dialect
        from sqlalchemy.dialects.mysql import base
        base.dialect = self.default_dialect

    def readfile(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        return io.open(path, encoding='utf-8').read()

    def test_basic(self):
        engine = sqlalchemy.create_engine(self.mysqld.url())
        engine.execute(self.readfile('schema/mysql_basic.sql'))

        try:
            fd, output = tempfile.mkstemp()
            os.close(fd)

            rst.main(['-o', output, self.config.name])
            self.assertEqual(self.readfile('rst/mysql_basic.rst'),
                             io.open(output, encoding='utf-8').read())

            graph.main(['-o', output, self.config.name])
            self.assertEqual(self.readfile('rst/mysql_basic_graph.rst'),
                             io.open(output, encoding='utf-8').read())
        finally:
            os.unlink(output)
