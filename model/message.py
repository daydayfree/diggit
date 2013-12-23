# -*- coding: utf-8 -*-

from datetime import datetime
from bson import ObjectId

from model.user import User
from model.photo import Photo


STATUS_UNREAD = 'unread'
STATUS_READ = 'read'


class Message(object):

    table = 'message'

    def __init__(self, id, to_id, photo_id, from_ids, kind, update_time, status):
        self.id = id
        self.to_id = to_id
        self.photo_id = photo_id
        self.froms_id = froms_id
        self.kind = kind
        self.update_time = update_time
        self.status = status

    @property
    def subscriber(self):
        return self.to_id and User.get(self.to_id)

    @property
    def creators(self):
        return self.from_ids and [User.get(fid) for fid in self.from_ids]

    @property
    def photo(self):
        return self.photo_id and Photo.get(self.photo_id)

    @property
    def count(self):
        return len(self.from_ids)

    @classmethod
    def new(cls, to_id, photo_id, from_id, kind, create_time, status=STATUS_UNREAD):
        query = {
            'photo_id': photo_id,
            'status': STATUS_UNREAD,
            'kind': kind
        }
        item = get_cursor(cls.table).find_one(query)
        if not item:
            item = {
                'to_id': to_id,
                'photo_id': photo_id,
                'from_ids': [from_id],
                'kind': kind,
                'update_time': create_time,
                'status': status
            }
            get_cursor(cls.table).insert(item, safe=True)
        else:
            id = item.get('_id')
            from_ids = set(item.get('from_ids', []))
            from_ids.add(from_id)
            query = {'_id': id}
            update = {'from_ids': list(from_ids)}
            get_cursor(cls.table).update(query, {'$set': update}, safe=True)

    @classmethod
    def read(cls, id):
        query = {'_id': ObjectId(id)}
        update = {'status': STATUS_READ}
        get_cursor(cls.table).update(query, {'$set': update}, safe=True)

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        id = str(item.get('_id', ''))
        to_id = item.get('to_id')
        photo_id = item.get('photo_id')
        from_ids = item.get('from_ids', [])
        kind = item.get('kind')
        update_time = item.get('update_time')
        status = item.get('status')
        if not (id and to_id and from_ids and photo_id):
            return None
        return cls(id, to_id, photo_id, from_ids, kind, update_time, status)

    @classmethod
    def gets_by_user(cls, to_id):
        query = {
            'to_id': to_id
            'status': STATUS_UNREAD
        }
        rs = get_cursor(cls.table).find(query).sort('update_time', -1)
        return filter(None, [cls.initialize(r) for r in rs])

    @classmethod
    def get_count_by_user(cls, to_id):
        query = {
            'to_id': to_id
            'status': STATUS_UNREAD
        }
        return get_cursor(cls.table).find(query).count()
