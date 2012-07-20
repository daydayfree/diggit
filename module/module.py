#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

class AccountModule(tornado.web.UIModule):
    def render(self, user):
        return self.render_string("modules/account.html", user=user)


class NoticeModule(tornado.web.UIModule):
    def render(self, notice):
        return self.render_string("modules/notice.html", notice=notice)
        

class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)


class UserBoardModule(tornado.web.UIModule):
    def render(self, user, followed):
        return self.render_string("modules/user_board.html", user=user,
                                  followed=followed)


class UserProfileModule(tornado.web.UIModule):
    def render(self, user, followed):
        return self.render_string("modules/user_profile.html", user=user,
                                  followed=followed)


class PersonModule(tornado.web.UIModule):
    def render(self, user, odd):
        return self.render_string("modules/person.html", user=user, odd=odd)


class PagerModule(tornado.web.UIModule):
    def render(self, pager):
        return self.render_string("modules/pager.html", pager=pager)


class CommentModule(tornado.web.UIModule):
    def render(self, comment):
        return self.render_string(
            "modules/comment.html", comment=comment)


class HeaderModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/header.html")


class CategoriesBarModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/categories_bar.html")
