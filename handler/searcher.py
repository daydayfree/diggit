# -*- coding: utf-8 -*-

from base import BaseHandler

class SearchHandler(BaseHandler):
    def get(self):
        q = self.get_argument("q", None)
        if not q: self.redirect("/")
        index = int(self.get_argument("p", "1"))
        index = 1 if index < 1 else index
        self.render("search.html", q = q, p = index)
