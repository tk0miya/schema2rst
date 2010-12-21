# -*- coding: utf-8 -*-

import re
import common


class Inspector(common.Inspector):
    def __init__(self, bind):
        super(Inspector, self).__init__(bind)
        self.bind.execute('SET NAMES utf8')

    def get_tables(self, **kw):
        tables = super(Inspector, self).get_tables(**kw)
        for table in tables:
            query = """SELECT TABLE_COMMENT
                       FROM information_schema.Tables
                       WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'""" % \
                       (self.default_schema_name, table['name'])
            r = self.bind.execute(query).fetchone()

            table['fullname'] = re.sub('; Inno.*$', '', self.decode(r[0]))

        return tables

    def get_foreign_keys_for_column(self, table_name, column_name, *kw):
        fk = self.get_foreign_keys(table_name, *kw)
        return [k for k in fk if column_name in k['constrained_columns']]

    def get_columns(self, table_name, **kw):
        columns = super(Inspector, self).get_columns(table_name, **kw)
        for column in columns:
            query = """SELECT COLUMN_TYPE, COLLATION_NAME,
                              EXTRA, COLUMN_COMMENT
                       FROM information_schema.Columns
                       WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' AND
                             COLUMN_NAME = '%s'""" % \
                       (self.default_schema_name, table_name, column['name'])
            r = self.bind.execute(query).fetchone()
            column['type'] = self.decode(r[0])

            options = []
            collation_name = self.decode(r[1])
            if collation_name and collation_name != 'utf8_general_ci':
                options.append(collation_name)

            extra = self.decode(r[2])
            if extra:
                options.append(extra)

            if self.get_foreign_keys_for_column(table_name, column['name']):
                fk = self.get_foreign_keys_for_column(table_name, column['name'])
                for key in fk:
                    for refcolumn in key['referred_columns']:
                        msg = "FK: %s.%s" % (key['referred_table'], refcolumn)
                        options.append(msg)

            comment = self.decode(r[3])
            extra_comment = ", ".join(options)
            match = re.match('^(.*?)(?:\(|¡Ê)(.*)(?:\)|¡Ë)\s*$', comment)
            if match:
                column['fullname'] = match.group(1)
                column['comment'] = match.group(2)

                if extra_comment:
                    column['comment'] += " (%s)" % extra_comment
            elif comment:
                column['fullname'] = comment
                column['comment'] = extra_comment
            else:
                column['fullname'] = column['name']
                column['comment'] = extra_comment

        return columns
