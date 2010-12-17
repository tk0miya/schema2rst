# -*- coding: utf-8 -*-

import os
import sqlalchemy
from sphinx import SphinxDocGenerator
from pit import Pit


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

        schema_name = os.path.basename(str(self.engine.url))
        query = """SELECT COLUMN_COMMENT
                   FROM information_schema.Columns
                   WHERE TABLE_SCHEMA = '%s' AND
                         TABLE_NAME = '%s' AND
                         COLUMN_NAME = '%s'""" % \
                   (schema_name, self.meta.table.name, self.name)
        rs = self.engine.execute(query)
        self.comment = rs.fetchone()[0]

    def reflect(self, engine):
        self.engine = engine

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
        return self.meta.default

    @property
    def doc(self):
        return self.meta.doc or ""


def main():
    config = Pit.get('gmappers', {'require': {'host': 'localhost',
                                              'user': 'gmappers',
                                              'passwd': '',
                                              'db': 'gmappers'}})

    url = 'mysql://%s:%s@%s/%s' % \
          (config['user'], config['passwd'], config['host'], config['db'])
    engine = sqlalchemy.create_engine(url)

    m = MySQLMetaData()
    m.reflect(engine)

    sphinx = SphinxDocGenerator()
    sphinx.header(u'Schema: %s' % config['db'])

    for table in m.tables.values():
        sphinx.header(table.name, '-')

        headers = ['Fullname', 'Name', 'Type', 'NOT NULL',
                   'PKey', 'Default', 'Comment']
        sphinx.listtable(headers)

        for c in table.columns:
            columns = [c.fullname, c.name, c.type, c.nullable,
                       c.primary_key, c.default, c.doc]
            sphinx.listtable_column(columns)


if __name__ == '__main__':
    main()
