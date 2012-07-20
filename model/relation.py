#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename: model/relation.py


from model import Model
from notice import Notice


class Relation(Model):
    table = "relations"

    @property
    def notice_dal(self): return Notice()

    def save(self, follow):
        follow_id = self.insert(follow)
        if not follow_id: return

        if follow["follower_id"] == follow["user_id"]:
            return

        notice = {
            "_id": self.notice_dal.get_id(),
            "user_id": follow["follower_id"],
            "user": self.dbref("users", follow["follower_id"]),
            "subscriber_id": follow["user_id"],
            "subscriber": self.dbref("users", follow["user_id"]),
            "published": follow["published"],
            "notice_type": "follow"
        }
        self.notice_dal.save(notice)
        return follow_id


    def get_relation(self, follower_id, user_id):
        parameters = {"follower_id": follower_id, "user_id": user_id}
        return self.get(parameters)


    def remove_relation(self, follower_id, user_id):
        parameters = {"follower_id": follower_id, "user_id": user_id}
        self.remove(parameters)

        
    def get_followers_count(self, user_id):
        parameters = {"user_id": user_id}
        return self.get_count(parameters)

    def get_followers(self, user_id, offset=0, limit=10):
        followers = []
        parameters = {"user_id": user_id}
        result = self.query(parameters, offset, limit, fields=['follower'])

        if result and len(result):
            followers = [ r["follower"] for r in result ]
        return followers


    def get_follower_ids(self, user_id, offset=0, limit=10):
        ids = []
        parameters = {"user_id": user_id}
        result = self.query(parameters, offset, limit, fields="follower_id")
        if result and len(result):
            ids = [r["follower_id"] for r in result]
        return ids


    def get_friends_count(self, user_id):
        parameters = {"follower_id": user_id}
        return self.get_count(parameters)


    def get_friends(self, user_id, offset=0, limit=0):
        friends = []
        parameters = {"follower_id": user_id}
        result = self.query(parameters, offset, limit, fields=["user"])

        if result and len(result):
            friends = [r["user"] for r in result]
        return friends

    def get_relations_by_ids(self, follower_id, ids):
        parameters = {"follower_id": follower_id, "user_id": {"$in": ids}}
        result = self.query(parameters, 0, len(ids), fields=["user_id"])
        return [u["user_id"] for u in result]
