# coding: utf-8

import tornado.web

from model.photo import Photo
from view import BaseHandler

class FavHandler(BaseHandler):


    @tornado.web.authenticated
    def post(self):
        photo_id = self.get_argument('photo_id','')
        print photo_id
        photo = Photo.get(photo_id)
        photo.inc_like_count()
        self.redirect('/')
