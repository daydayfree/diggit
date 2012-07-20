#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename: model/comment.py

from model import Model
from feed import Feed
from notice import Notice


class Comment(Model):
    table = "comments"

    @property
    def notice_dal(self): return Notice()

    @property
    def feed_dal(self): return Feed()

    def save(self, comment):
        comment_id = self.insert(comment)
        if not comment_id: return
        """
        feed = self.feed_dal.get_last_feed(comment["user_id"], "comment")
        if not feed:
            feed = {
                "_id": self.feed_dal.get_id(),
                "user_id": comment["user_id"],
                "user": self.dbref("users", comment["user_id"]),
                "published": comment["published"],
                "entries": [self.dbref("entries", comment["entry_id"])],
                "feed_type": "comment",
                "entry_type": "image"
            }
            self.feed_dal.save(feed)
        else:
            if len(feed["entries"]):
                feed["entries"] = [self.dbref("entries", e["_id"]) 
                                   for e in feed["entries"]]
            feed["entries"].append(self.dbref("entries", comment["entry_id"]))
            feed["user"] = self.dbref("users", feed["user_id"])
            parameters = {"_id": feed["_id"]}
            self.feed_dal.update(parameters, feed)
        """
        """
        if comment["user_id"] == comment["subscriber_id"]:
            return comment_id
        notice = {
            "_id": self.notice_dal.get_id(),
            "user_id": comment["user_id"],
            "user": self.dbref("users", comment["user_id"]),
            "subscriber_id": comment["subscriber_id"],
            "entry_id": comment["entry_id"],
            "entry": self.dbref("entries", comment["entry_id"]),
            "published": comment["published"],
            "notice_type": "comment",
            "content": comment["content"],
            "entry_type": "image",
            "readed": 0
        }
        self.notice_dal.save(notice)
        """
        return comment_id


    def get_comments(self, entry_id, offset=0, limit=10):
        parameters = {"entry_id": entry_id}
        comments = self.query(parameters, offset=offset, limit=limit)
        if not comments: return None
        return [comment for comment in comments]

    def get_comments_count(self, entry_id):
        parameters = {"entry_id": entry_id}
        return self.get_count(parameters)


    def delete_comment(self, comment_id):
        pass


    def delete_entry_comments(self, entry_id):
        pass


    def get_comments_by_ids(self, tweetIds):
        parameters = {"entry_id": {"$in": tweetIds}}
        return self.query(parameters, 0, 100)
        

