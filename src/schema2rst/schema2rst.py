# -*- coding: utf-8 -*-

import os
import sys
import yaml
import sqlalchemy
import inspectors
from sphinx import SphinxDocGenerator


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: schema2rst CONFIG_FILE\n')
        sys.exit(1)

    config = yaml.load(file(sys.argv[1]))

    url = 'mysql://%s:%s@%s/%s' % \
          (config['user'], config['passwd'], config['host'], config['db'])
    engine = sqlalchemy.create_engine(url)

    insp = inspectors.create_inspector(engine)

    sphinx = SphinxDocGenerator()
    sphinx.header(u'Schema: %s' % config['db'])

    for table in insp.get_table_names():
        # FIXME: support fullname (table comment)
        sphinx.header(table, '-')

        headers = ['Fullname', 'Name', 'Type', 'NOT NULL',
                   'PKey', 'Default', 'Comment']
        sphinx.listtable(headers)

        for c in insp.get_columns(table):
            columns = [c.get('fullname'), c.get('name'), c.get('type'), c.get('nullable'),
                       c.get('primary_key'), c.get('default'), c.get('comment')]
            sphinx.listtable_column(columns)

        indexes = insp.get_indexes(table)
        if indexes:
            sphinx.header(u'Keys', '^')
            for index in indexes:
                if index['unique']:
                    string = "UNIQUE KEY: %s (%s)" % (index['name'], ', '.join(index['column_names']))
                else:
                    string = "KEY: %s (%s)" % (index['name'], ', '.join(index['column_names']))


if __name__ == '__main__':
    main()
