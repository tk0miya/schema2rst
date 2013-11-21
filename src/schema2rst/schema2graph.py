# -*- coding: utf-8 -*-

import io
import sys
import six
import yaml
import sqlalchemy
import inspectors
from rst import RestructuredTextGenerator


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: schema2rst CONFIG_FILE\n')
        sys.exit(1)

    config = yaml.load(io.open(sys.argv[1], encoding='utf-8'))

    url = 'mysql://%s:%s@%s/%s' % \
          (config['user'], config['passwd'], config['host'], config['db'])
    engine = sqlalchemy.create_engine(url)

    insp = inspectors.create_inspector(engine)

    doc = RestructuredTextGenerator()
    doc.header(six.u('Schema: %s' % config['db']))

    doc.out(".. graphviz::")
    doc.out("")
    doc.out("   digraph {")
    doc.out("      node [shape = box];")

    for table in insp.get_tables():
        if table['fullname']:
            doc.out('      %s [label="%s\\n(%s)"];' %
                    (table['name'], table['name'], table['fullname']))
        else:
            doc.out('      %s;' % table['name'])

        for key in insp.get_foreign_keys(table['name']):
            doc.out('      %s -> %s;' %
                    (table['name'], key['referred_table']))

    doc.out("   }")


if __name__ == '__main__':
    main()
