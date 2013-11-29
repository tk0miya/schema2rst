# -*- coding: utf-8 -*-

import io
import sys
import yaml
import optparse
from schema2rst import inspectors
from schema2rst.rstwriter import RestructuredTextWriter


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
    engine = inspectors.create_engine(config)
    try:
        inspector = inspectors.create_for(engine)

        doc = RestructuredTextWriter(options.output)
        generate_doc(doc, inspector, config)
    finally:
        engine.dispose()


def generate_doc(doc, inspector, config):
    doc.header('Schema: %s' % config['db'])

    doc.println(".. graphviz::")
    doc.println("")
    doc.println("   digraph {")
    doc.println("      node [shape = box];")

    for table in inspector.get_tables():
        if table['fullname']:
            doc.println('      %s [label="%s\\n(%s)"];' %
                        (table['name'], table['name'], table['fullname']))
        else:
            doc.println('      %s;' % table['name'])

        for key in inspector.get_foreign_keys(table['name']):
            doc.println('      %s -> %s;' %
                        (table['name'], key['referred_table']))

    doc.println("   }")
    doc.close()
