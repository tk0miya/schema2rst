# -*- coding: utf-8 -*-

import sqlalchemy
from schema2rst.inspectors import common, mysql, pgsql


def create_engine(config):
    schema = config.get('type', 'mysql')
    if 'unix_socket' in config:
        url = ('%s://%s:%s@localhost/%s?unix_socket=%s' %
               (schema, config['user'], config['passwd'],
                config['db'], config['unix_socket']))
    else:
        url = ('%s://%s:%s@%s:%d/%s' %
               (schema, config['user'], config['passwd'],
                config['host'], config['port'], config['db']))

    return sqlalchemy.create_engine(url)


def create_for(engine):
    if engine.driver in ('mysqldb', 'pymysql'):
        return mysql.Inspector(engine)
    elif engine.driver in ('psycopg2',):
        return pgsql.Inspector(engine)
    else:
        return common.Inspector(engine)
