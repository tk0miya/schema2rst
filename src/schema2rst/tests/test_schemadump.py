# -*- coding: utf-8 -*-

import io
import os
import unittest
import tempfile
import sqlalchemy
import testing.mysqld

from schema2rst.commands import dump


class TestSchemadump(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 65535
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

    def create_engine(self):
        url = self.mysqld.url()
        if '?' in url:
            url += '&charset=utf8'
        else:
            url += '?charset=utf8'

        return sqlalchemy.create_engine(url)

    def test_dump(self):
        engine = self.create_engine()
        engine.execute(self.readfile('schema/mysql_basic.sql'))
        engine.dispose()

        try:
            fd, output = tempfile.mkstemp()
            os.close(fd)

            dump.main(['-c', self.config.name, '-o', output])
            self.assertEqual(self.readfile('yaml/mysql_basic.yaml'),
                             io.open(output, encoding='utf-8').read())
        finally:
            os.unlink(output)

    def test_dump_comment(self):
        engine = self.create_engine()
        engine.execute(self.readfile('schema/mysql_comments.sql'))
        engine.dispose()

        try:
            fd, output = tempfile.mkstemp()
            os.close(fd)

            dump.main(['-c', self.config.name, '-o', output])
            self.assertEqual(self.readfile('yaml/mysql_comments.yaml'),
                             io.open(output, encoding='utf-8').read())
        finally:
            os.unlink(output)