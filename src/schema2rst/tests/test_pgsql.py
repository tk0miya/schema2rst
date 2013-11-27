# -*- coding: utf-8 -*-

import io
import os
import unittest
import tempfile
import sqlalchemy
import testing.postgresql

from schema2rst.commands import graph, rst


class TestSchema2rst(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 65535
        self.pgsql = testing.postgresql.Postgresql()

        param = self.pgsql.dsn()
        self.config = tempfile.NamedTemporaryFile('w+')
        self.config.write("type: postgresql\n")
        self.config.write("db: %s\n" % param['dbname'])
        self.config.write("user: %s\n" % param['user'])
        self.config.write("passwd: \"\"\n")
        self.config.write("host: %s\n" % param['host'])
        self.config.write("port: %s" % param['port'])
        self.config.flush()

    def readfile(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        return io.open(path, encoding='utf-8').read()

    def create_engine(self):
        url = self.mysqld.url()
        return sqlalchemy.create_engine(url)

    def test_basic(self):
        try:
            engine = sqlalchemy.create_engine(self.pgsql.url())
            engine.execute(self.readfile('schema/pgsql_basic.sql'))
        finally:
            engine.dispose()

        try:
            fd, output = tempfile.mkstemp()
            os.close(fd)

            rst.main(['-o', output, self.config.name])
            self.assertEqual(self.readfile('rst/pgsql_basic.rst'),
                             io.open(output, encoding='utf-8').read())

            graph.main(['-o', output, self.config.name])
            self.assertEqual(self.readfile('rst/pgsql_basic_graph.rst'),
                             io.open(output, encoding='utf-8').read())
        finally:
            os.unlink(output)

    def test_with_comments(self):
        try:
            engine = sqlalchemy.create_engine(self.pgsql.url())
            engine.execute(self.readfile('schema/pgsql_comments.sql'))
        finally:
            engine.dispose()

        try:
            fd, output = tempfile.mkstemp()
            os.close(fd)

            rst.main(['-o', output, self.config.name])
            self.assertEqual(self.readfile('rst/pgsql_comments.rst'),
                             io.open(output, encoding='utf-8').read())

            graph.main(['-o', output, self.config.name])
            self.assertEqual(self.readfile('rst/pgsql_comments_graph.rst'),
                             io.open(output, encoding='utf-8').read())
        finally:
            os.unlink(output)
