# -*- coding: utf-8 -*-

from schema2rst.inspectors import common, mysql


def create_inspector(engine):
    if engine.driver == 'mysqldb':
        return mysql.Inspector(engine)
    else:
        return common.Inspector(engine)
