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
from sqlalchemy.engine.reflection import Inspector


class Column(dict):
    def set_comment(self, comment, options=[]):
        extra_comment = ", ".join(options)
        match = re.match('^(.*?)(?:\(|（)(.*)(?:\)|）)\s*$', comment)
        if match:
            self['fullname'] = match.group(1).strip()
            self['comment'] = match.group(2).strip()

            if extra_comment:
                self['comment'] += " (%s)" % extra_comment
        elif comment:
            self['fullname'] = comment.strip()
            self['comment'] = extra_comment.strip()
        else:
            self['fullname'] = self['name']
            self['comment'] = extra_comment.strip()


class SimpleInspector(Inspector):
    def __init__(self, bind):
        super(SimpleInspector, self).__init__(bind)

    def get_tables(self, **kw):
        tables = []
        table_names = super(SimpleInspector, self).get_table_names(**kw)
        for table_name in sorted(table_names):
            table = {'name': table_name, 'fullname': ''}
            tables.append(table)

        return tables

    def get_columns(self, table_name, **kw):
        constraints = self.get_pk_constraint(table_name)
        primary_keys = constraints.get('constrained_columns')
        columns = super(SimpleInspector, self).get_columns(table_name, **kw)

        # wrap column objects in Column class
        columns = [Column(c) for c in columns]

        for column in columns:
            column['fullname'] = column['name']
            column['comment'] = ''

            if column['name'] in primary_keys:
                column['primary_key'] = True
            else:
                column['primary_key'] = False

        return columns
