# -*- coding: utf-8 -*-

import json

from model.photo import Photo
from view import BaseHandler


class IndexPhotoHandler(BaseHandler):

    def post(self):
        start = self.get_argument('start', 0)
        photos = Photo.gets(0, 20)

        # TODO
        # liked by current user

        html = []
        for photo in photos:
            i = self.render_string('modules/photo.html', photo=photo)
            html.append(i)

        # TODO
        # continue fetching
        end = False

        r = dict(code=200, end=end, photos=html)
        self.write(json.dumps(r))
