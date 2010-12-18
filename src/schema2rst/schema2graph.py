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

    sphinx.out(".. graphviz::")
    sphinx.out("")
    sphinx.out("   digraph {")
    sphinx.out("      node [shape = box];")

    for table in insp.get_tables():
        if table['fullname']:
            sphinx.out('      %s [label="%s\\n(%s)"];' % \
                       (table['name'], table['name'], table['fullname']))
        else:
            sphinx.out('      %s;' % table['name'])

        for key in insp.get_foreign_keys(table['name']):
            sphinx.out('      %s -> %s;' % \
                       (table['name'], key['referred_table']))

    sphinx.out("   }")


if __name__ == '__main__':
    main()
