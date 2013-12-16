# -*- coding: utf-8 -*-

from bson import ObjectId

from corelib.store import get_cursor
from model.notice import Notice
from model.entry import Entry


class User(object):

    table = 'user'

    def __init__(self, id, name, email, city, blog='', intro='', uid=''):
        self.id = id
        self.name = name
        self.email = email
        self.city = city
        self.blog = blog
        self.intro = intro
        self.uid = uid or id

    @property
    def photo_count(self):
        pass

    @property
    def like_count(self):
        pass

    @property
    def following_count(self):
        pass

    @property
    def followed_count(self):
        pass

    @classmethod
    def get(cls, id):
        query = {'_id': ObjectId(id)}
        item = get_cursor(cls.table).find_one(query)

        if not item:
            return None
        id = str(item.get('_id', ''))
        name = item.get('name', '')
        email = item.get('email')
        city = item.get('city', '')
        blog = item.get('blog', '')
        intro = item.get('intro', '')
        uid = item.get('uid') or id

        if not email:
            return None
        return cls(id, name, email, city, blog, intro, uid)

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
