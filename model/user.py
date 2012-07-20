#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename: model/user.py

from model import Model
from notice import Notice
from entry import Entry

class User(Model):
    table = "users"

    def template(self):
        user = {
            "_id": self.get_id(),
            "name": '', 
            "email": '', 
            "city": '', 
            "open": '', 
            "remote_ip": '', 
            "domain": '',
            "photo_url": '', 
            "middle_photo_url": '', 
            "bio": '', 
            "username": '', 
            "link": '',
            "entries": 0, 
            "likes": 0, 
            "followers": 0, 
            "friends": 0
        }
        return user

    @property
    def entry_dal(self): return Entry()


    def update_user(self, user):
        parameters = {"_id": user["_id"]}
        return self.update(parameters, user)


    def get_user(self, user_id):
        parameters = {"_id": int(user_id)}
        return self.get(parameters)

    
    def get_users(self, offset=0, limit=10):
        parameters = None
        return self.query(parameters, offset=offset, limit=limit)


    def get_users_count(self):
        parameters = None
        return self.get_count(parameters)


    def get_top_entries(self, user_id):
        return self.entry_dal.get_user_top_entries(user_id)


    def update_entries_count(self, user_id, increment=1):
        parameters = {"_id": user_id}
        self.update(parameters, {"$inc": {"entries": increment}})


    def update_likes_count(self, user_id, increment=1):
        parameters = {"_id": user_id}
        self.update(parameters, {"$inc": {"likes": increment}})


    def update_followers_count(self, user_id, increment=1):
        parameters = {"_id": user_id}
        self.update(parameters, {"$inc": {"followers": increment}})


    def update_friends_count(self, user_id, increment=1):
        parameters = {"_id": user_id}
        self.update(parameters, {"$inc": {"friends": increment}})
