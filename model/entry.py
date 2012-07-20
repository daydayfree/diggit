#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename: model/entry.py

import datetime
from model import Model
from feed import Feed
from notice import Notice
from comment import Comment


class Entry(Model):
    table = "entries"

    def template(self):
        entry = {
            "_id": self.get_id(),
            "user_id": "",
            "user": "",
            "title": "",
            "link": "",
            "profile": "",
            "tags": [],
            "description": "",
            "source": "",
            "thumb": "",
            "middle": "",
            "height": 0,
            "width": 0,
            "md5": "",
            "size": "",
            "published": datetime.datetime.now(),
            "updated": self.timestamp,
            "comments": 0,
            "likes": 0,
            "categories": "",
            "_keywords": ""
        }
        return entry

    @property
    def comment_dal(self): return Comment()

    @property
    def feed_dal(self): return Feed()

    @property
    def fav_dal(self): return Fav()

    def save(self, tweet):
        return self.insert(tweet)
        """
        feed = self.feed_dal.get_last_feed(entry["user_id"], "upload")

        if not feed:
            feed = {
                "_id": self.feed_dal.get_id(),
                "user_id": entry["user_id"],
                "user": self.dbref("users", entry["user_id"]),
                "entries": [self.dbref("entries", entry["_id"])],
                "published": entry["published"],
                "feed_type": "upload",
                "entry_type": "image"
            }
            self.feed_dal.save(feed)
        else:
            if feed["entries"] and len(feed["entries"]):
                feed["entries"] = [self.dbref("entries", e["_id"]) 
                                   for e in feed["entries"]
                                   if e["_id"] != entry["_id"]]
            feed["entries"].append(self.dbref("entries", entry["_id"]))
            feed["user"] = self.dbref("users", feed["user_id"])
            parameters = {"_id": feed["_id"]}
            self.feed_dal.update(parameters, feed)
        """


    def update_comments_count(self, tweetid, inc=1):
        parameters = {"_id": tweetid}
        self.update(parameters, {"$inc": {"comments": inc}})


    def update_likes_count(self, tweetid, inc=1):
        parameters = {"_id": tweetid}
        self.update(parameters, {"$inc": {"likes": inc}})


    def get_user_entries_count(self, user_id):
        paramters = {"user_id": user_id}
        return self.get_count(paramters)


    def get_user_entries(self, user_id, offset=0, limit=10):
        parameters = {"user_id": user_id}
        return self.query(parameters, offset, limit)


    def get_comments(self, entry_id, offset=0, limit=10):
        comments = self.comment_dal.get_comments(entry_id, offset, limit)
        return comments


    def get_comments_count(self, entry_id):
        return self.comment_dal.get_comments_count(entry_id)


    def delete_comments(self, entry_id):
        self.comment_dal.delete_entry_comments(entry_id)


    def get_entry(self, entry_id):
        parameters = { "_id": entry_id }
        entry = self.db.find_one(self.table, parameters)
        return entry

    
    def get_primary_entries(self, user_id, published):
        parameters = {"published": {"$lte": published}, "user_id": user_id}
        prev_result = self.query(parameters, limit=4)

        parameters = {"published": {"$gt": published}, "user_id": user_id}
        next_result = self.query(parameters, limit=4)

        return {"next": next_result, "pre": prev_result}

    
    def get_user_top_entries(self, user_id, limit=4):
        parameters = {"user_id": user_id}
        return self.query(parameters, limit=limit)


    def get_entries_by_category(self, category, offset=0, limit=10):
        parameters = {"categories": category}
        return self.query(parameters, offset=offset, limit=limit)

    def get_entries_count_by_category(self, category):
        parameters = {"categories": category}
        return self.get_count(parameters)
