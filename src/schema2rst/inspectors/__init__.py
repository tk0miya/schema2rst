# -*- coding: utf-8 -*-

from sqlalchemy.engine.reflection import Inspector


def create_inspector(engine):
    return Inspector(engine)
