#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import datetime
from model import Model
from relation import Relation

NEAR_TIMESTAMP = 7200

class Feed(Model):
    """
    1.Friend upload a photo or blog or album
    2.Friend like a photo or blog or album
    3.Friend comment a photo or blog or album
    """

    table = "feeds"

    @property
    def relation(self): return Relation()


    def save(self, feed):
        return self.insert(feed)


    def get_feeds(self, user_id, offset, limit):
        pass


    def get_last_feed(self, user_id, feed_type):
        parameters = {"user_id": user_id, "feed_type": feed_type}
        timestamp = time.time()
        d = datetime.datetime.fromtimestamp(timestamp - NEAR_TIMESTAMP)
        parameters["published"] = {"$gt": d}
        return self.get(parameters)

