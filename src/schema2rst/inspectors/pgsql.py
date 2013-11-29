# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from schema2rst.inspectors.base import SimpleInspector


class PgSQLInspector(SimpleInspector):
    def get_tables(self):
        query = ("""SELECT c.relname, obj_description(c.oid, 'pg_class')
                    FROM pg_class c
                    LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
                    WHERE c.relkind = 'r' AND n.nspname = '%s'""" %
                 self.default_schema_name)
        fullnames = dict(self.bind.execute(query).fetchall())

        tables = super(PgSQLInspector, self).get_tables()
        for table in tables:
            table['fullname'] = fullnames.get(table['name'])

        return tables

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

        columns = super(PgSQLInspector, self).get_columns(table_name, **kw)
        for column in columns:
            options = []

            for key in column['foreign_keys']:
                for refcolumn in key['referred_columns']:
                    msg = "FK: %s.%s" % (key['referred_table'], refcolumn)
                    options.append(msg)

            comment = comments.get(column['name']) or ''
            column.set_comment(comment, options)

        return columns
