# -*- coding: utf-8 -*-

import re
import common

class Inspector(common.Inspector):
    def __init__(self, bind):
        super(Inspector, self).__init__(bind)

    def get_tables(self, **kw):
        tables = super(Inspector, self).get_tables(**kw)
        for table in tables:
            query = """SELECT TABLE_COMMENT
                       FROM information_schema.Tables
                       WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'""" % \
                       (self.default_schema_name, table['name'])
            r = self.bind.execute(query).fetchone()

            table['fullname'] = self.decode(r[0])

        return tables

    def get_columns(self, table_name, **kw):
        columns = super(Inspector, self).get_columns(table_name, **kw)
        for column in columns:
            query = """SELECT COLLATION_NAME, COLUMN_TYPE, EXTRA, COLUMN_COMMENT
                       FROM information_schema.Columns
                       WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' AND
                             COLUMN_NAME = '%s'""" % \
                       (self.default_schema_name, table_name, column['name'])
            r = self.bind.execute(query).fetchone()

            column['collation_name'] = self.decode(r[0])
            column['type'] = self.decode(r[1])
            column['extra'] = self.decode(r[2])
            column['comment'] = self.decode(r[3])

            comment = self.decode(r[3])
            match = re.match('^(.*?)(?:\(|¡Ê)(.*)(?:\)|¡Ë)\s*$', comment)
            if match:
                column['fullname'] = match.group(1)
                column['comment'] = match.group(2)
            elif comment:
                column['fullname'] = comment
                column['comment'] = ''
            else:
                column['fullname'] = column['name']
                column['comment'] = ''

        return columns
