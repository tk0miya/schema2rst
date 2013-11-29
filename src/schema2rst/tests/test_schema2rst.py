# -*- coding: utf-8 -*-

import io
import os
import tempfile
from mock import patch

from schema2rst.commands import rst

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestSchema2rst(unittest.TestCase):
    def readfile(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        return io.open(path, encoding='utf-8').read()

    @patch("optparse.OptionParser.error")
    def test_parse_option(self, error):
        if sys.version_info < (2, 7):  # skip tests in py2.6
            return

        error.side_effect = RuntimeError  # do not output error to stderr

        # no arguments
        with self.assertRaises(RuntimeError):
            rst.parse_option([])

        # no -c/-o options
        with self.assertRaises(RuntimeError):
            rst.parse_option(['-o', 'output.rst'])

        # both -c and -o
        with self.assertRaises(RuntimeError):
            rst.parse_option(['-c', 'config.yaml', '-d', 'dump.yaml',
                              '-o', 'output.rst'])

        # success (1)
        option, args = rst.parse_option(['-c', 'config.yaml',
                                         '-o', 'output.rst'])
        self.assertEqual('config.yaml', option.config)
        self.assertEqual(None, option.datafile)
        self.assertEqual('output.rst', option.output)
        self.assertEqual([], args)

        # success (2)
        option, args = rst.parse_option(['-d', 'dump.yaml',
                                         '-o', 'output.rst'])
        self.assertEqual(None, option.config)
        self.assertEqual('dump.yaml', option.datafile)
        self.assertEqual('output.rst', option.output)
        self.assertEqual([], args)

    def test_from_datafile_basic(self):
        try:
            fd, output = tempfile.mkstemp()
            os.close(fd)

            datafile = os.path.join(os.path.dirname(__file__),
                                    'yaml/mysql_basic.yaml')
            rst.main(['-d', datafile, '-o', output])
            self.assertEqual(self.readfile('rst/mysql_basic.rst'),
                             io.open(output, encoding='utf-8').read())
        finally:
            os.unlink(output)

    def test_from_datafile_comment(self):
        try:
            fd, output = tempfile.mkstemp()
            os.close(fd)

            datafile = os.path.join(os.path.dirname(__file__),
                                    'yaml/mysql_comments.yaml')
            rst.main(['-d', datafile, '-o', output])
            self.assertEqual(self.readfile('rst/mysql_comments.rst'),
                             io.open(output, encoding='utf-8').read())
        finally:
            os.unlink(output)
