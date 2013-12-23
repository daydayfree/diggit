# -*- coding: utf-8 -*-

import tornado.web
from model.user import User
from model.kind import Kind


class BaseHandler(tornado.web.RequestHandler):

    @property
    def current_user(self):
        user_id = self.get_secure_cookie('user')
        if not user_id:
            return None
        return User.get(user_id)

    @property
    def categories(self):
        return Kind.gets()

    def get_hot_tags(self, start=0, limit=10):
        return []
