# -*- coding: utf-8 -*-

from sqlalchemy.engine import reflection


class Inspector(reflection.Inspector):
    def __init__(self, bind):
        super(Inspector, self).__init__(bind)

    def decode(self, string):
        if string:
            return string.decode('utf-8')
        else:
            return string

    def get_tables(self, **kw):
        tables = []
        table_names = super(Inspector, self).get_table_names(**kw)
        for table_name in table_names:
            table = {'name': table_name, 'fullname': ''}
            tables.append(table)

        return tables

    def get_columns(self, table_name, **kw):
        primary_keys = self.get_primary_keys(table_name)
        columns = super(Inspector, self).get_columns(table_name, **kw)
        for column in columns:
            column['fullname'] = column['name']
            column['comment'] = ''

            if column['name'] in primary_keys:
                column['primary_key'] = True
            else:
                column['primary_key'] = False

        return columns
