# -*- coding: utf-8 -*-

import re
from schema2rst.inspectors import common


class Inspector(common.Inspector):
    def get_tables(self):
        query = ("""SELECT c.relname, obj_description(c.oid, 'pg_class')
                    FROM pg_class c
                    LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE c.relkind = 'r' AND n.nspname = '%s'""" %
                 self.default_schema_name)
        fullnames = dict(self.bind.execute(query).fetchall())

        tables = super(Inspector, self).get_tables()
        for table in tables:
            table['fullname'] = fullnames.get(table['name'])

        return tables

    def get_foreign_keys_for_column(self, table_name, column_name, *kw):
        fk = self.get_foreign_keys(table_name, *kw)
        return [k for k in fk if column_name in k['constrained_columns']]

    def get_columns(self, table_name, **kw):
        query = ("""SELECT a.attname, col_description(a.attrelid, a.attnum)
                    FROM pg_attribute a
                    LEFT JOIN pg_class c ON c.oid = a.attrelid
                    LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE
                      c.relkind = 'r' AND a.attnum > 0 AND
                      NOT a.attisdropped AND
                      n.nspname = '%s' AND relname = '%s'""" %
                 (self.default_schema_name, table_name))
        comments = dict(self.bind.execute(query).fetchall())

        columns = super(Inspector, self).get_columns(table_name, **kw)
        for column in columns:
            options = []

            fk = self.get_foreign_keys_for_column(table_name, column['name'])
            if fk:
                for key in fk:
                    for refcolumn in key['referred_columns']:
                        msg = "FK: %s.%s" % (key['referred_table'], refcolumn)
                        options.append(msg)

            comment = comments.get(column['name']) or ''
            extra_comment = ", ".join(options)
            match = re.match('^(.*?)(?:\(|（)(.*)(?:\)|）)\s*$', comment)
            if match:
                column['fullname'] = match.group(1).strip()
                column['comment'] = match.group(2).strip()

                if extra_comment:
                    column['comment'] += " (%s)" % extra_comment
            elif comment:
                column['fullname'] = comment.strip()
                column['comment'] = extra_comment.strip()
            else:
                column['fullname'] = column['name']
                column['comment'] = extra_comment.strip()

        return columns
