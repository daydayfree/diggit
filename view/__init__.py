# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from corelib.filestore import fs
from model.user import User
from model.kind import Kind


class BaseHandler(RequestHandler):

    def get_current_user(self):
        user_id = self.get_secure_cookie('uid')
        if not user_id:
            return None
        return User.get(user_id)

    @property
    def categories(self):
        return Kind.gets()

    def get_hot_tags(self, start=0, limit=10):
        return []


class ImageRenderHandler(RequestHandler):

    def get(self, category, filename):
        self.add_header('content-type', 'image/jpeg')
        self.write(fs.load(filename, category))


def photo_url(category, filename):
    from application import application
    return application.reverse_url('image_render', category, filename)
