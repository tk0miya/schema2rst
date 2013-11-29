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

import sqlalchemy
from schema2rst.inspectors import common, mysql, pgsql


def create_engine(config):
    schema = config.get('type', 'mysql')
    if 'unix_socket' in config:
        url = ('%s://%s:%s@localhost/%s?unix_socket=%s' %
               (schema, config['user'], config['passwd'],
                config['db'], config['unix_socket']))

        if schema == 'mysql':
            url += "&charset=utf8"
    else:
        url = ('%s://%s:%s@%s:%d/%s' %
               (schema, config['user'], config['passwd'],
                config['host'], config['port'], config['db']))

        if schema == 'mysql':
            url += "?charset=utf8"

    return sqlalchemy.create_engine(url)


def create_for(engine):
    if engine.driver in ('mysqldb', 'pymysql'):
        return mysql.Inspector(engine)
    elif engine.driver in ('psycopg2',):
        return pgsql.Inspector(engine)
    else:
        return common.Inspector(engine)
