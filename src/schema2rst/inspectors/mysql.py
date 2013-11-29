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

import re
from schema2rst.inspectors.base import SimpleInspector


class MySQLInspector(SimpleInspector):
    def get_tables(self, **kw):
        tables = super(MySQLInspector, self).get_tables(**kw)
        for table in tables:
            query = ("""SELECT TABLE_COMMENT
                        FROM information_schema.Tables
                        WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'""" %
                     (self.default_schema_name, table['name']))
            r = self.bind.execute(query).fetchone()

            table['fullname'] = re.sub('; InnoDB.*$', '', r[0])
            if table['fullname'].startswith('InnoDB'):
                table['fullname'] = None

        return tables

    def get_columns(self, table_name, **kw):
        columns = super(MySQLInspector, self).get_columns(table_name, **kw)
        for column in columns:
            query = ("""SELECT COLUMN_TYPE, COLLATION_NAME,
                               EXTRA, COLUMN_COMMENT
                        FROM information_schema.Columns
                        WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' AND
                              COLUMN_NAME = '%s'""" %
                     (self.default_schema_name, table_name, column['name']))
            r = self.bind.execute(query).fetchone()
            column['type'] = r[0]

            options = []
            collation_name = r[1]
            if collation_name and collation_name != 'utf8_general_ci':
                options.append(collation_name)

            extra = r[2]
            if extra:
                options.append(extra)

            for key in column['foreign_keys']:
                for refcolumn in key['referred_columns']:
                    msg = "FK: %s.%s" % (key['referred_table'], refcolumn)
                    options.append(msg)

            column.set_comment(r[3], options)

        return columns
