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

    def get_columns(self, table_name, **kw):
        columns = super(Inspector, self).get_columns(table_name, **kw)
        for column in columns:
            column['fullname'] = column['name']
            column['comment'] = ''

        return columns
