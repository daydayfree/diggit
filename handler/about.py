# -*- coding: utf-8 -*-

import tornado.web
from base import BaseHandler

class AboutHandler(BaseHandler):
    def get(self):
        self.render("about.html")

    
class HelpHanlder(BaseHandler):
    def get(self):
        self.render("help.html")


class TermHandler(BaseHandler):
    def get(self):
        self.render("term.html")
