# -*- coding: utf-8 -*-

import os
import re
import sqlalchemy


def decode(string):
    if string:
        return string.decode('utf-8')
    else:
        return string


class MySQLMetaData:
    def __init__(self):
        self.meta = sqlalchemy.MetaData()
        self.engine = None

    def reflect(self, engine):
        self.engine = engine
        self.meta.reflect(engine)

    @property
    def tables(self):
        _tables = {}
        for table_name in self.meta.tables:
            table = MySQLTable(self.meta.tables[table_name])
            table.reflect(self.engine)
            _tables[table_name] = table

        return _tables


class MySQLTable:
    def __init__(self, meta):
        self.meta = meta

    def reflect(self, engine):
        self.engine = engine

    @property
    def name(self):
        return self.meta.name

    @property
    def columns(self):
        for column in self.meta.columns:
            column = MySQLColumn(column)
            column.reflect(self.engine)
            yield column


class MySQLColumn:
    def __init__(self, meta):
        self.meta = meta
        self.comment = None

    def reflect(self, engine):
        self.engine = engine

        schema_name = os.path.basename(str(self.engine.url))
        query = """SELECT COLUMN_COMMENT, COLUMN_DEFAULT
                   FROM information_schema.Columns
                   WHERE TABLE_SCHEMA = '%s' AND
                         TABLE_NAME = '%s' AND
                         COLUMN_NAME = '%s'""" % \
                   (schema_name, self.meta.table.name, self.name)
        rs = self.engine.execute(query)
        row = rs.fetchone()
        self.comment = decode(row[0])
        self.default = decode(row[1])

    @property
    def fullname(self):
        return self.comment or self.meta.name

    @property
    def name(self):
        return self.meta.name

    @property
    def type(self):
        return self.meta.type

    @property
    def nullable(self):
        return self.meta.nullable

    @property
    def primary_key(self):
        return self.meta.primary_key

    @property
    def default(self):
        return self.default

    @property
    def doc(self):
        return self.meta.doc or ""
