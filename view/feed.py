# -*- coding: utf-8 -*-

import tornado.web
from model import Notice
from base import BaseHandler
from util import Log, Pager


class FeedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("feed.html")


class NoticeHandler(BaseHandler):
    @property
    def notice_dal(self): return Notice()

    @tornado.web.authenticated
    def get(self):
        notices = self.notice_dal.get_notices(self.current_user["_id"])
        self.render("notice.html", notices=notices)
