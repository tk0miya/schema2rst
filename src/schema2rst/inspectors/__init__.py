# -*- coding: utf-8 -*-

import sqlalchemy
from schema2rst.inspectors import common, mysql


def create_for(config):
    if 'unix_socket' in config:
        url = ('mysql://%s:%s@localhost/%s?unix_socket=%s' %
               (config['user'], config['passwd'],
                config['db'], config['unix_socket']))
    else:
        url = ('mysql://%s:%s@%s/%s' %
               (config['user'], config['passwd'],
                config['host'], config['db']))

    engine = sqlalchemy.create_engine(url)
    if engine.driver == 'mysqldb':
        return mysql.Inspector(engine)
    else:
        return common.Inspector(engine)
