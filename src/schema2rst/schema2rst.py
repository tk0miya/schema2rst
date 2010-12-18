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

    for table in insp.get_tables():
        # FIXME: support fullname (table comment)
        if table['fullname']:
            sphinx.header("%s (%s)" % (table['fullname'], table['name']), '-')
        else:
            sphinx.header(table['name'], '-')

        headers = ['Fullname', 'Name', 'Type', 'NOT NULL',
                   'PKey', 'Default', 'Comment']
        sphinx.listtable(headers)

        for c in insp.get_columns(table['name']):
            columns = [c.get('fullname'), c.get('name'), c.get('type'),
                       c.get('nullable'), c.get('primary_key'),
                       c.get('default'), c.get('comment')]
            sphinx.listtable_column(columns)

        indexes = insp.get_indexes(table['name'])
        if indexes:
            sphinx.header(u'Keys', '^')
            for index in indexes:
                if index['unique']:
                    format = "UNIQUE KEY: %s (%s)"
                else:
                    format = "KEY: %s (%s)"

                string = format % (index['name'],
                                   ', '.join(index['column_names']))
                sphinx.list_item(string)


if __name__ == '__main__':
    main()
