# -*- coding: utf-8 -*-

from datetime import datetime
from bson import ObjectId

from corelib.store import get_cursor
from model.photo import Photo
from model.user import User


class Comment(object):

    table = 'comment'

    def __init__(self, id, photo_id, author_id, text, create_time):
        self.id = id
        self.photo_id = photo_id
        self.author_id = author_id
        self.text = text
        self.create_time = create_time

    @property
    def author(self):
        return self.author_id and User.get(self.author_id)

    @property
    def photo(self):
        return self.photo_id and Photo.get(self.photo_id)

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        id = str(item.get('_id'))
        photo_id = item.get('photo_id')
        author_id = item.get('author_id')
        text = item.get('text')
        create_time = item.get('create_time')
        return cls(id, photo_id, author_id, text, create_time)

    @classmethod
    def get(cls, id):
        query = {'_id': ObjectId(id)}
        item = get_cursor(cls.table).find_one(query)
        return cls.initialize(item)

    @classmethod
    def gets_by_photo(cls, photo_id, start=0, limit=10):
        query = {'photo_id': photo_id}
        rs = get_cursor(cls.table).find(query).sort('create_time', -1)\
                                  .skip(start).limit(limit)
        return filter(None, [cls.initialize(r) for r in rs])

    @classmethod
    def get_count_by_photo(cls, photo_id):
        query = {'photo_id': photo_id}
        return get_cursor(cls.table).find(query).count()

    @classmethod
    def new(cls, photo_id, author_id, text):
        item = {
            'photo_id': photo_id,
            'author_id': author_id,
            'text': text,
            'create_time': datetime.now()
        }
        id = get_cursor(cls.table).insert(item, safe=True)
        if id:
            return cls.get(id)
        return None

    @classmethod
    def delete(cls, id):
        query = {'_id': ObjectId(id)}
        get_cursor(cls.table).remove(query, safe=True)

    @classmethod
    def gets(cls, ids):
        query = {'_id': {'$in': [ObjectId(id) for id in ids]}}
        rs = get_cursor(cls.table).find(query)
        return filter(None, [cls.initialize(r) for r in rs])

