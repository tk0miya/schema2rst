# -*- coding: utf-8 -*-

import io
import sys
import yaml
import optparse
from schema2rst import inspectors
from schema2rst.rst import RestructuredTextGenerator


def parse_option(args):
    usage = 'Usage: schema2rst CONFIG_FILE'
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

        doc = RestructuredTextGenerator(options.output)
        generate_doc(doc, inspector, config)
    finally:
        engine.dispose()


def generate_doc(doc, inspector, config):
    doc.header('Schema: %s' % config['db'])

    for table in inspector.get_tables():
        # FIXME: support fullname (table comment)
        if table['fullname']:
            doc.header("%s (%s)" %
                       (table['fullname'], table['name']), '-')
        else:
            doc.header(table['name'], '-')

        headers = ['Fullname', 'Name', 'Type', 'NOT NULL',
                   'PKey', 'Default', 'Comment']
        doc.listtable(headers)

        for c in inspector.get_columns(table['name']):
            columns = [c.get('fullname'), c.get('name'), c.get('type'),
                       (not c.get('nullable')), c.get('primary_key'),
                       c.get('default'), c.get('comment')]
            doc.listtable_column(columns)

        indexes = inspector.get_indexes(table['name'])
        if indexes:
            doc.header('Keys', '^')
            for index in indexes:
                if index['unique']:
                    format = "UNIQUE KEY: %s (%s)"
                else:
                    format = "KEY: %s (%s)"

                string = format % (index['name'],
                                   ', '.join(index['column_names']))
                doc.list_item(string)
