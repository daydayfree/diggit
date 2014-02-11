# coding: utf-8

from model.photo import Photo
from view import BaseHandler


class LikeHandler(BaseHandler):

    def post(self):
        photo_id = self.get_argument('photo_id', '')
        photo = Photo.get(photo_id)
        photo.inc_like_count()
        self.set_header("Content-Type", "application/json")
        r = {
            'code': 200,
            'like_count': photo.like_count,
            'photo_id': photo_id
        }
        self.write(r)
        self.finish()

