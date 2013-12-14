# -*- coding: utf-8 -*-

import tornado.web
from model import User, Category, Tag
from util import TimeDeltaFormat


class BaseHandler(tornado.web.RequestHandler):
    @property
    def user_dal(self): return User()

    @property
    def category_dal(self): return Category()

    @property
    def tag_dal(self): return Tag()

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.user_dal.get_user(int(user_id))


    def render_error(self, *args, **kwargs):
        header = "application/x-javascript; charset=utf-8"
        self.set_header("Content-Type", header)
        self.render("ajax/error.json", args, kwargs)


    def get_photo_url(self, user, size="normal"):
        if not user:
            return self.static_url("default.png")

        photo = "photo_url" if size == "normal" else "middle_photo_url"
        if photo not in user and user[photo]:
            photo = "photo_url"

        if not user[photo]:
            return self.static_url("images/default.png")
        if "open" in user and user["open"] != "google":
            if user[photo].startswith("http"):
                return user[photo]
        return self.static_url("icons/%s" % user[photo])


    def date_format(self, date):
        return TimeDeltaFormat.format(date)


    def get_all_categories(self):
        return self.category_dal.get_all()


    def get_tags(self, offset=0, limit=20):
        return self.tag_dal.get_tags(offset, limit)
