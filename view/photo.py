# -*- coding: utf-8 -*-

import tornado.web

from view import BaseHandler
from model.photo import Photo


class UploadHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        return self.render('photo/upload.html')

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        text = self.get_argument('text', '')
        kinds = self.get_arguments('kinds', [])
        tags = self.get_argument('tags', '')
        f = self.request.files.get('file')
        content = f[0].body if f else None

        if not content:
            self.render('photo/upload.html')
        if tags:
            tags = tags.split(',')
        Photo.new(text, kinds, tags, user.id, content)
        self.redirect('/')
