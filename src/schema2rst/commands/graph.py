# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import io
import sys
import yaml
import optparse
from schema2rst import inspectors
from schema2rst.rstwriter import RestructuredTextWriter


def parse_option(args):
    usage = 'Usage: schema2graph CONFIG_FILE'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-c', '--config', action='store')
    parser.add_option('-d', '--datafile', action='store')
    parser.add_option('-o', '--output', action='store')

    options, args = parser.parse_args(args)
    if options.config is None and options.datafile is None:
        parser.error('--config (-c) or --datafile (-d) is required')

    if options.config and options.datafile:
        parser.error('Specify either --config (-c) or --datafile (-d)')

    return options, args


def main(args=sys.argv[1:]):
    options, args = parse_option(args)

    if options.datafile:
        schema = yaml.safe_load(open(options.datafile))
    else:
        try:
            config = yaml.load(io.open(options.config, encoding='utf-8'))
            engine = inspectors.create_engine(config)
            schema = inspectors.create_for(engine).dump()
        finally:
            engine.dispose()

    doc = RestructuredTextWriter(options.output)
    generate_doc(doc, schema)


def generate_doc(doc, schema):
    doc.header('Schema: %s' % schema['name'])

    doc.println(".. graphviz::")
    doc.println("")
    doc.println("   digraph {")
    doc.println("      node [shape = box];")

    for table in schema['tables']:
        if table['fullname']:
            doc.println('      %s [label="%s\\n(%s)"];' %
                        (table['name'], table['name'], table['fullname']))
        else:
            doc.println('      %s;' % table['name'])

        for key in table['foreign_keys']:
            doc.println('      %s -> %s;' %
                        (table['name'], key['referred_table']))

    doc.println("   }")
    doc.close()
