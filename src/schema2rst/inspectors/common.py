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

from sqlalchemy.engine import reflection


class Inspector(reflection.Inspector):
    def __init__(self, bind):
        super(Inspector, self).__init__(bind)

    def get_tables(self, **kw):
        tables = []
        table_names = super(Inspector, self).get_table_names(**kw)
        for table_name in sorted(table_names):
            table = {'name': table_name, 'fullname': ''}
            tables.append(table)

        return tables

    def get_columns(self, table_name, **kw):
        constraints = self.get_pk_constraint(table_name)
        primary_keys = constraints.get('constrained_columns')
        columns = super(Inspector, self).get_columns(table_name, **kw)
        for column in columns:
            column['fullname'] = column['name']
            column['comment'] = ''

            if column['name'] in primary_keys:
                column['primary_key'] = True
            else:
                column['primary_key'] = False

        return columns
