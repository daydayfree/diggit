# -*- coding: utf-8 -*-

import pymongo
from settings import MONGODB_CONFIG


mongo = pymongo.Connection("mongodb://%s" % MONGODB_CONFIG['HOST'],
                           port=MONGODB_CONFIG['PORT'],
                           network_timeout=15)
db = mongo.diggit


def get_cursor(table):
    return getattr(db, table)
