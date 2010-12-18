# -*- coding: utf-8 -*-

import common
import mysql


def create_inspector(engine):
    if engine.driver == 'mysqldb':
        return mysql.Inspector(engine)
    else:
        return common.Inspector(engine)
