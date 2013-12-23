# -*- coding: utf-8 -*-

from datetime import datetime
from bson import ObjectId

from corelib.store import get_cursor
from model.user import User


class TweetMixin(object):

    kind = None


