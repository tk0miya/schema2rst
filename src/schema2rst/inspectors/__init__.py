# -*- coding: utf-8 -*-

import inspector
import mysql


def create_inspector(engine):
    if engine.driver == 'mysqldb':
        return mysql.Inspector(engine)
    else:
        return inspector.Inspector(engine)
