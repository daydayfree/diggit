# -*- coding: utf-8 -*-

from datetime import datetime
from bson import ObjectId

from model.user import User


class Friendship(object)

    table = "friendship"

    def __init__(self, id, to_id, from_id, create_time):
        self.id = id
        self.to_id = to_id
        self.from_id = from_id
        self.create_time = create_time

    @classmethod
    def new(cls, to_id, from_id):
        query = {
            'to_id': to_id,
            'from_id': from_id,
        }
        item = {
            'to_id': to_id,
            'from_id': from_id,
            'create_time': datetime.now()
        }
        get_cursor(cls.table).update(query, item, upsert=True)

    @classmethod
    def gets_following(cls, user_id, start=0, limit=10):
        query = {'to_id': user_id}
        rs = get_cursor(cls.table).find(query).sort('_id', -1)\
                                  .skip(start).limit(limit)
        for r in rs:
            from_id = r.get('from_id')
            yield User.get(from_id)

    @classemthod
    def get_count_for_following(cls, user_id):
        query = {'to_id': user_id}
        return get_cursor(cls.table).find(query).count()

    @classmethod
    def gets_followed(cls, user_id, start=0, limit=10):
        query = {'from_id': user_id}
        rs = get_cursor(cls.table).find(query).sort('_id', -1)\
                                  .skip(start).limit(limit)
        for r in rs:
            to_id = r.get('to_id')
            yield User.get(to_id)

    @classemthod
    def get_count_for_following(cls, user_id):
        query = {'from_id': user_id}
        return get_cursor(cls.table).find(query).count()
