# -*- coding: utf-8 -*-

from datetime import datetime
from bson import ObjectId
from corelib.store import get_cursor


class User(object):

    table = 'user'

    def __init__(self, id, name, email, city, blog='', intro='', uid='',
                 create_time=None, update_time=None):
        self.id = id
        self.name = name
        self.email = email
        self.city = city
        self.blog = blog
        self.intro = intro
        self.uid = uid or id
        self.create_time = create_time
        self.update_time = update_time

    def __repr__(self):
        return '<user:%s,name=%s>' % (self.id, self.name)

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
    def new(cls, name, email, city='', blog='', intro='', uid=''):
        current_time = datetime.now()
        item = {
            'name': name,
            'email': email,
            'city': city,
            'blog': blog,
            'intro': intro,
            'uid': uid,
            'create_time': current_time,
            'update_time': current_time
        }
        id = get_cursor(cls.table).insert(item, safe=True)
        if id:
            return cls.get(id)
        return None

    def update_password(self, password):
        query = {'user_id': self.id}
        update = {
            'user_id': self.id,
            'password': password,
            'update_time': datetime.now()
        }
        get_cursor('user_password').update(query, update, upsert=True)

    def get_password(self):
        query = {'user_id': self.id}
        r = get_cursor('user_password').find_one(query)
        return r and r.get('password')

    @classmethod
    def initialize(cls, item):
        if not item:
            return None
        id = str(item.get('_id', ''))
        name = item.get('name', '')
        email = item.get('email')
        city = item.get('city', '')
        blog = item.get('blog', '')
        intro = item.get('intro', '')
        uid = item.get('uid') or id
        create_time = item.get('create_time')
        update_time = item.get('update_time')
        if not email:
            return None
        return cls(id, name, email, city, blog, intro, uid, create_time, update_time)

    @classmethod
    def get(cls, id):
        query = {'_id': ObjectId(id)}
        item = get_cursor(cls.table).find_one(query)
        return item and cls.initialize(item)

    @classmethod
    def get_by_uid(cls, uid):
        query = {'uid': uid}
        item = get_cursor(cls.table).find_one(query)
        return item and cls.initialize(item)

    @classmethod
    def get_by_email(cls, email):
        query = {'email': email}
        item = get_cursor(cls.table).find_one(query)
        return item and cls.initialize(item)

    def update(self, name='', city='', blog='', intro='', uid=''):
        query = {'_id': ObjectId(self.id)}
        update = {}
        if name:
            update['name'] = name
        if city:
            update['city'] = city
        if blog:
            update['blog'] = blog
        if intro:
            update['intro'] = intro
        if uid:
            update['uid'] = uid
        if update:
            update['update_time'] = datetime.now()
            get_cursor(self.table).update(query, {'$set': update}, safe=True)
        return User.get(self.id)

    @classmethod
    def gets(cls, start=0, limit=10):
        rs = get_cursor(cls.table).find('update_time', -1).sort()\
                                  .skip(start).limit(limit)
        return filter(None, [cls.initialize(r) for r in rs])

    @classmethod
    def get_count(cls):
        return get_cursor(cls.table).count()

    @property
    def avatar_url(self, category='thumb'):
        # TODO
        return 'http://img3.douban.com/icon/u3146440-17.jpg'
