# -*- coding: utf-8 -*-

import io
import sys
import six
import yaml
import optparse
import inspectors
from rst import RestructuredTextGenerator


def parse_option(args):
    usage = 'Usage: schema2graph CONFIG_FILE'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-o', '--output', action='store')

    options, args = parser.parse_args(args)
    if len(args) != 1:
        parser.print_usage()
        sys.exit(0)

    return options, args


def main(args=sys.argv[1:]):
    options, args = parse_option(args)

    config = yaml.load(io.open(args[0], encoding='utf-8'))
    insp = inspectors.create_for(config)

    doc = RestructuredTextGenerator(options.output)
    doc.header(six.u('Schema: %s' % config['db']))

    doc.out(six.u(".. graphviz::"))
    doc.out(six.u(""))
    doc.out(six.u("   digraph {"))
    doc.out(six.u("      node [shape = box];"))

    for table in insp.get_tables():
        if table['fullname']:
            doc.out(six.u('      %s [label="%s\\n(%s)"];') %
                    (table['name'], table['name'], table['fullname']))
        else:
            doc.out(six.u('      %s;') % table['name'])

        for key in insp.get_foreign_keys(table['name']):
            doc.out(six.u('      %s -> %s;') %
                    (table['name'], key['referred_table']))

    doc.out(six.u("   }"))
