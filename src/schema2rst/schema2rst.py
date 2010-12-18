# -*- coding: utf-8 -*-

import os
import sys
import yaml
import sqlalchemy
from metadata import MySQLMetaData
from sphinx import SphinxDocGenerator


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: schema2rst CONFIG_FILE\n')
        sys.exit(1)

    config = yaml.load(file(sys.argv[1]))

    url = 'mysql://%s:%s@%s/%s' % \
          (config['user'], config['passwd'], config['host'], config['db'])
    engine = sqlalchemy.create_engine(url)

    m = MySQLMetaData()
    m.reflect(engine)

    sphinx = SphinxDocGenerator()
    sphinx.header(u'Schema: %s' % config['db'])

    for table in m.tables.values():
        if table.fullname:
            header = u"%s (%s)" % (table.fullname, table.name)
            sphinx.header(header, '-')
        else:
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
