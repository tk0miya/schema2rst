# -*- coding: utf-8 -*-

import sqlalchemy
from schema2rst.inspectors import common, mysql


def create_for(url):
    engine = sqlalchemy.create_engine(url)
    if engine.driver == 'mysqldb':
        return mysql.Inspector(engine)
    else:
        return common.Inspector(engine)
