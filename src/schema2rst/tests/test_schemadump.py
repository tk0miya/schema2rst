# -*- coding: utf-8 -*-

import io
import os
import tempfile
import sqlalchemy
import testing.mysqld

from schema2rst.commands import dump

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


@testing.mysqld.skipIfNotInstalled
class TestSchemadump(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 65535
        self.mysqld = testing.mysqld.Mysqld(my_cnf={'skip-networking': None})

        param = self.mysqld.dsn()
        self.config = tempfile.NamedTemporaryFile('w+')
        self.config.write("type: mysql+pymysql\n")
        self.config.write("db: %s\nuser: %s\npasswd: \"\"\nunix_socket: %s\n" %
                          (param['db'], param['user'], param['unix_socket']))
        self.config.flush()

    def readfile(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        return io.open(path, encoding='utf-8').read()

    def test_dump(self):
        engine = sqlalchemy.create_engine(self.mysqld.url(charset='utf8'))
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
        engine = sqlalchemy.create_engine(self.mysqld.url(charset='utf8'))
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
