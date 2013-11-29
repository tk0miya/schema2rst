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
import six
import sys
import yaml
import optparse
from schema2rst import inspectors


def parse_option(args):
    usage = 'Usage: schemadump [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-c', '--config', action='store')
    parser.add_option('-o', '--output', action='store')

    options, args = parser.parse_args(args)

    if options.config is None:
        parser.error('--config (-c) is required')

    return options, args


def main(args=sys.argv[1:]):
    options, args = parse_option(args)

    config = yaml.load(io.open(options.config, encoding='utf-8'))
    try:
        engine = inspectors.create_engine(config)
        schema = inspectors.create_for(engine).dump()
    finally:
        engine.dispose()

    try:
        if options.output:
            output = io.open(options.output, 'w', encoding='utf-8')
        else:
            output = io.open(sys.stdout.fileno(), 'w', encoding='utf-8')

        output.write(serialize(schema))
    finally:
        output.close()


def serialize(data):
    ret = yaml.safe_dump(data)
    if isinstance(ret, six.binary_type):
        ret = ret.decode('utf-8')

    return ret
