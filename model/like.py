# -*- coding: utf-8 -*-

from datetime import datetime
from bson import ObjectId

from corelib.store import get_cursor
from model.photo import Photo
from model.user import User


class Like(object):

    table = "photo_like"

    def __init__(self, id, photo_id, author_id, create_time):
        self.id = id
        self.photo_id = photo_id
        self.author_id = author_id
        self.create_time = create_time

    @property
    def photo(self):
        return self.photo_id and Photo.get(self.photo_id)

    @property
    def author(self):
        return self.author_id and User.get(self.author_id)

    @classmethod
    def new(cls, photo_id, author_id):
        item = {
            'photo_id': photo_id,
            'author_id': author_id,
            'create_time': datetime.now()
        }
        id = get_cursor(cls.table).insert(item, safe=True)
        if id:
            return cls.get(id)
        return None

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        id = str(item.get('_id', ''))
        photo_id = item.get('photo_id')
        author_id = item.get('author_id')
        create_time = item.get('create_time')
        if not (id and photo_id and author_id):
            return None
        return cls(id, photo_id, author_id, create_time)

    @classmethod
    def get(cls, id):
        query = {'_id': ObjectId(id)}
        item = get_cursor(cls.table).find_one(query)
        return cls.initialize(item)

    @classmethod
    def gets(cls, start=0, limit=10):
        rs = get_cursor(cls.table).find().sort('create_time', 1)\
                                  .skip(start).limit(limit)
        return filter(None, [cls.initialize(r) for r in rs])

    @classmethod
    def get_count(cls):
        return get_cursor(cls.table).find(query).count()

    @classmethod
    def gets_by_user(cls, user_id, start=0, limit=10):
        query = {'author_id': author_id}
        rs = get_cursor(cls.table).find(query).sort('create_time')\
                                  .skip(start).limit(limit)
        return cls.initialize(item)

    @classmethod
    def get_count_by_user(cls, user_id):
        query = {'author_id': author_id}
        return get_cursor(cls.table).find(query).count()

    @classmethod
    def gets_by_photo(cls, photo_id, start=0, limit=10):
        query = {'photo_id': photo_id}
        rs = get_cursor(cls.table).find(query).sort('create_time')\
                                  .skip(start).limit(limit)
        return cls.initialize(item)

    @classmethod
    def get_count_by_photo(cls, photo_id):
        query = {'photo_id': photo_id}
        return get_cursor(cls.table).find(query).count()
