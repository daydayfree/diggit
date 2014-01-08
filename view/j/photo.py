# -*- coding: utf-8 -*-

import json

from corelib.consts import MAX_PHOTO_COUNT
from model.photo import Photo
from view import BaseHandler


class IndexPhotoHandler(BaseHandler):

    def post(self):
        start = self.get_argument('start', '0')
        page = self.get_argument('page', '1')

        start = int(start) if start.isdigit() else 0
        page = int(page) if page.isdigit() else 1

        total = Photo.get_count()
        pages = total / MAX_PHOTO_COUNT
        if total % MAX_PHOTO_COUNT != 0:
            pages += 1

        cur_page_start = (page - 1) * MAX_PHOTO_COUNT
        if page > pages or (page == pages and cur_page_start + start == total):
            r = dict(code=400, photos=[])
            self.write(json.dumps(r))
            self.finish()
            return

        photos = Photo.gets(start, 10)

        # TODO
        # liked by current user

        html = []
        for photo in photos:
            i = self.render_string('modules/photo.html', photo=photo)
            html.append(i)

        r = dict(code=200, photos=html)
        self.write(json.dumps(r))
        self.finish()
