# -*- coding: utf-8 -*-

import tornado.web

from datetime import datetime
from model.user import User
from view import BaseHandler


class UserHandler(BaseHandler):

    def get(self, uid):
        user = User.get(uid)
        if not user:
            self.redirect('/404')
            return

        # TODO liked
        page = self.get_argument('page', '1')
        page = int(page) if page.isdigit() else 1

        self.render('user.html', user=user, page=page)
