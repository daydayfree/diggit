# -*- coding: utf-8 -*-

from utils.pager import Pager
from model.user import User
from model.photo import Photo

from base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        page = self.get_argument('p', '1')
        if not (page and page.isdigit()):
            page = 1
        else:
            page = int(page)
        self.render("index.html", p=page)


class CategoryHandler(BaseHandler):
    def get(self):
        index = int(self.get_argument("p", "1"))
        index = 1 if index < 1 else index
        category = self.get_argument("category", "1")
        self.render("all.html", p=index, category=category)


class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")

