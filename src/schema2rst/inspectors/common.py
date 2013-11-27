# -*- coding: utf-8 -*-

import six
from sqlalchemy.engine import reflection


class Inspector(reflection.Inspector):
    def __init__(self, bind):
        super(Inspector, self).__init__(bind)

    def decode(self, string):
        if isinstance(string, six.binary_type):
            return string.decode('utf-8')
        else:
            return string

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
