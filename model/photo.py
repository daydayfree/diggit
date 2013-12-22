# -*- coding: utf-8 -*-

from bson import ObjectId

from corelib.store import get_cursor
from model.user import User


class Photo(object):

    table = 'photo'

    def __init__(self, id, text, height, width, kinds, author_id,
                 create_time, update_time, like_count=0, comment_count=0):
        self.id = id
        self.text = text
        self.height = height
        self.width = width
        self.kinds = kinds
        self.author_id = author_id
        self.create_time = create_time
        self.update_time = update_time
        self.like_count = like_count
        self.comment_count = comment_count

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        id = str(item.get('_id', ''))
        text = item.get('text', '')
        height = item.get('height', 400)
        width = item.get('width', 220)
        kinds = item.get('kinds', [])
        author_id = item.get('author_id')
        create_time = item.get('create_time')
        update_time = item.get('update_time')
        like_count = item.get('like_count', 0)
        comment_count = item.get('comment_count', 0)

        if not (id and author_id and create_time):
            return None

        return cls(id, text, height, width, kinds, author_id, create_time,
                   update_time, like_count, comment_count)

    @classmethod
    def get(cls, id):
        query = {'_id': ObjectId(id)}
        item = get_cursor(cls.table).find_one(query)
        return cls.initialize(item)

    @classmethod
    def gets(cls, start=0, limit=10):
        rs = get_cursor(cls.table).find().sort('update_time', -1)\
                                  .skip(start).limit(limit)
        return filter(None, [cls.initialize(r) for r in rs])

    @classmethod
    def gets_by_user(cls, user_id, start=0, limit=10):
        query = {'author_id': user_id}
        rs = get_cursor(cls.table).find(query).sort('update_time', -1)\
                                  .skip(start).limit(limit)
        return filter(None, [cls.initialize(r) for r in rs])

    @property
    def author(self):
        return self.author_id and User.get(self.author_id)

