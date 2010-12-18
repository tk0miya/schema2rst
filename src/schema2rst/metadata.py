# -*- coding: utf-8 -*-

import os
import re


def decode(string):
    if string:
        return string.decode('utf-8')
    else:
        return string


class MySQLMetaData:
    def __init__(self):
        self.engine = None
        self.tables = {}

    def reflect(self, engine):
        self.name = os.path.basename(str(engine.url))

        query = """SELECT TABLE_NAME, TABLE_COMMENT
                   FROM information_schema.Tables
                   WHERE TABLE_SCHEMA = '%s'""" % self.name
        rs = engine.execute(query)
        for r in rs.fetchall():
            name = decode(r[0])
            fullname = decode(re.sub('(; )?InnoDB free.*$', '', r[1]))

            table = MySQLTable(self, [name, fullname])
            self.tables[name] = table

        for table_name in self.tables:
            self.tables[table_name].reflect(engine)

    def table(self, table_name):
        if hasattr(table_name, 'name'):
            table_name = table_name.name

        return self.tables[table_name]


class MySQLTable:
    def __init__(self, schema, row):
        self.schema = schema
        self.name = row[0]
        self.fullname = row[1]
        self.keys = []
        self.columns = []

    def reflect(self, engine):
        query = """SELECT COLUMN_NAME, COLUMN_DEFAULT, IS_NULLABLE,
                          COLLATION_NAME, COLUMN_TYPE, COLUMN_KEY,
                          EXTRA, COLUMN_COMMENT
                   FROM information_schema.Columns
                   WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'""" % \
                   (self.schema.name, self.name)
        rs = engine.execute(query)
        for r in rs.fetchall():
            column = MySQLColumn(self, r)
            self.columns.append(column)

        query = """SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
                   FROM information_schema.table_constraints
                   WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'""" % \
                   (self.schema.name, self.name)
        rs = engine.execute(query)
        for r in rs.fetchall():
            key = MySQLConstraint(r[0], self, r[1])
            key.reflect(engine)
            self.keys.append(key)

    def column(self, column_name):
        if hasattr(column_name, 'name'):
            column_name = column_name.name

        ret = [c for c in self.columns if c.name == column_name]
        if ret:
            return ret[0]
        else:
            return None

    def refkey(self, column):
        keys = [key for key in self.keys \
                if column in key.columns and key.type == 'FOREIGN KEY']
        if keys:
            return keys[0]
        else:
            return None


class MySQLConstraint:
    def __init__(self, name, table, type):
        self.name = name
        self.table = table
        self.type = type
        self.columns = []
        self.references = []

    def reflect(self, engine):
        query = """SELECT COLUMN_NAME, REFERENCED_TABLE_NAME,
                          REFERENCED_COLUMN_NAME
                   FROM information_schema.key_column_usage
                   WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s' AND
                         CONSTRAINT_NAME = '%s'""" % \
                   (self.table.schema.name, self.table.name, self.name)
        rs = engine.execute(query)
        schema = self.table.schema
        for r in rs.fetchall():
            self.columns.append(self.table.column(r[0]))
            if r[1]:
                reftable = schema.table(r[1])
                self.references.append(reftable.column(r[2]))


class MySQLColumn:
    def __init__(self, table, row):
        self.table = table

        self.name = row[0]
        self.default = decode(row[1])
        self.nullable = row[2]
        self.collation_name = row[3]
        self.type = row[4]
        self.primary_key = row[5] == 'PRI'
        self.unique_key = row[5] == 'UNI'
        self.extra = row[6]

        comment = decode(row[7])
        match = re.match('^(.*?)(?:\(|¡Ê)(.*)(?:\)|¡Ë)\s*$', comment)
        if match:
            self.fullname = match.group(1)
            self.comment = match.group(2)
        elif comment:
            self.fullname = comment
            self.comment = ''
        else:
            self.fullname = self.name
            self.comment = ''

    @property
    def doc(self):
        options = []

        if self.collation_name and self.collation_name != 'utf8_general_ci':
            options.append(self.collation_name)
        if self.extra:
            options.append(self.extra)
        if self.table.refkey(self):
            key = self.table.refkey(self)
            mesg = "Refer: %s" % key.references[0]
            options.append(mesg)

        if self.comment and options:
            return "%s (%s)" % (self.comment, ", ".join(options))
        elif options:
            return ", ".join(options)
        else:
            return self.comment
