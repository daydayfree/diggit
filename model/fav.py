#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename: model/fav.py

from model import Model
from feed import Feed
from notice import Notice
from user import User
from entry import Entry


class Fav(Model):
    table = "favs"

    @property
    def feed_dal(self): return Feed()

    @property
    def notice_dal(self): return Notice()

    @property
    def user_dal(self): return User()

    @property
    def entry_dal(self): return Entry()


    def get_faved_it(self, user_id, entry_id):
        parameters = {"user_id": user_id, "entry_id": entry_id}
        tmp = self.db.find_one(self.table, parameters)
        return True if tmp else False

    def get_favs(self, user_id, offset, limit):
        pass

    def save(self, fav):
        entry = self.entry_dal.get_entry(fav["entry_id"])
        if not entry: return

        fav_id = self.insert(fav)
        """
        feed = self.feed_dal.get_last_feed(fav["user_id"], "fav")
        if not feed:
            feed = {
                "_id": self.feed_dal.get_id(),
                "user_id": fav["user_id"],
                "user": self.dbref("users", fav["user_id"]),
                "published": fav["published"],
                "entries": [self.dbref("entries", fav["entry_id"])],
                "feed_type": "fav",
                "entry_type": "image"
            }
            self.feed_dal.save(feed)
        else:
            if feed["entries"] and len(feed["entries"]):
                feed["entries"] = [self.dbref("entries", e["_id"]) 
                                   for e in feed["entries"] 
                                   if e["_id"] != fav["entry_id"]]
            feed["entries"].append(self.dbref("entries", fav["entry_id"]))
            feed["user"] = self.dbref("users", feed["user_id"])
            parameters = {"_id": feed["_id"]}
            self.feed_dal.update(parameters, feed)
        """
        parameters = {"user_id": fav["user_id"], "entry_id": fav["entry_id"]}
        parameters["notice_type"] = "fav"
        notice = self.notice_dal.get(parameters)
        if notice: return fav_id

        if entry["user"]["_id"] == fav["user_id"]:
            return fav_id

        notice = {
            "_id": self.notice_dal.get_id(),
            "user_id": fav["user_id"],
            "user": self.dbref("users", fav["user_id"]),
            "entry_id": fav["entry_id"],
            "entry": self.dbref("entries", fav["entry_id"]),
            "subscriber_id": entry["user_id"],
            "published": fav["published"],
            "notice_type": "fav",
            "entry_type": "image",
            "readed": 0
        }
        self.notice_dal.save(notice)
        return fav_id


    def get_user_like_entries(self, user_id, offset=0, limit=10):
        parameters = {"user_id": user_id}
        fields = ["entry"]
        result = self.query(parameters, offset, limit, fields=fields)
        entries = []
        if result and len(result):
            entries = [e["entry"] for e in result]
        return entries

    
    def get_user_like_entries_count(self, user_id):
        parameters = {"user_id": user_id}
        return self.get_count(parameters)


    def get_entry_likers(self, tweet_id, limit=10):
        parameters = {"entry_id": tweet_id}
        result = self.query(parameters, 0, limit)
        return [f["user"] for f in result]


    def get_user_isliked(self, user_id, ids):
        params = {"user_id": user_id, "entry_id": {"$in": ids}}
        result = self.query(params, 0, len(ids), fields=["entry_id"])
        return [f["entry_id"] for f in result]
