# -*- coding: utf-8 -*-

import tornado.web
from view import BaseHandler


class AboutHandler(BaseHandler):
    def get(self):
        self.render("about.html")


class HelpHandler(BaseHandler):
    def get(self):
        self.render("help.html")


class TeamHandler(BaseHandler):
    def get(self):
        self.render("team.html")
