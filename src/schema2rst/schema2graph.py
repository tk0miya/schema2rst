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

    sphinx.out(".. graphviz::")
    sphinx.out("")
    sphinx.out("   digraph {")
    sphinx.out("      node [shape = box];")

    for table in m.tables.values():
        if table.fullname:
            sphinx.out('      %s [label="%s\\n(%s)"];' % \
                       (table.name, table.name, table.fullname))
        else:
            sphinx.out('      %s;' % table.name)

        for key in table.keys:
            if key.type == 'FOREIGN KEY':
                sphinx.out('      %s -> %s;' % \
                           (table.name, key.references[0].table.name))

    sphinx.out("   }")


if __name__ == '__main__':
    main()
