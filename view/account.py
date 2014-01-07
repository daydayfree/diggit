# -*- coding: utf-8 -*-

from tornado.web import authenticated

from utils import encrypt
from utils.image import crop_icon, save_origin_icon

from model.user import User
from view import BaseHandler


class SettingsHandler(BaseHandler):

    @authenticated
    def get(self):
        self.render("account/settings.html", error=None)

    @authenticated
    def post(self):
        user = self.current_user
        new_name = self.get_argument("name", user.name)
        new_city = self.get_argument("city", "")
        new_blog = self.get_argument("blog", "")
        new_intro = self.get_argument("intro", "")
        result = user.update(new_name, new_city, new_blog, new_intro)
        if result:
            self.render("account/settings.html", error=130)
            return
        self.render("account/settings.html", error=131)
        return


class PasswordHandler(BaseHandler):

    error_message = {
        "140": "密码修改成功。",
        "141": "原始密码填写错误。",
        "142": "新密码不能为空。",
        "143": "密码修改出错，请稍后再试。"
    }

    @authenticated
    def get(self):
        self.render("account/pwd.html", error=None)

    @authenticated
    def post(self):
        user = self.current_user
        password = self.get_argument("pwd", "")
        new_pwd = self.get_argument("new_pwd", "")
        if user.get_password() != encrypt(password):
            self.render("account/pwd.html", error=141)
            return
        if new_pwd == "":
            self.render("account/pwd.html", error=142)
            return
        result = user.update_password(encrypt(new_pwd))
        if result:
            self.render("account/pwd.html", error=143)
            return
        self.render("account/pwd.html", error=140)


class IconHandler(BaseHandler):

    error_message = {
        "150": "头像修改成功。",
        "151": "请选择头像。",
        "152": "图片格式不支持。",
        "153": "头像修改出错，请稍后再试。"
    }

    @authenticated
    def get(self):
        self.render("account/icon.html", error=None)

    @authenticated
    def post(self):
        if not self.request.files:
            self.render("account/icon.html", error=151)
            return
        files = self.request.files.get('icon')
        if not files:
            self.render("account/icon.html", error=151)
            return
        ext = files[0]["content_type"].split("/")[1]
        if ext not in ('jpeg', 'png', 'gif', 'jpg'):
            self.render("account/icon.html", error=152)
            return
        content = files[0].body
        save_origin_icon(self.current_user.avatar_filename, content)
        self.render("account/crop.html", error=None)


class CropIconHandler(BaseHandler):

    error_message = {
        "150": "头像设置成功。",
        "152": "头像设置出错，重新裁剪试试。"
    }

    @authenticated
    def get(self):
        if not self.current_user.has_origin_avatar():
            self.redirect("/settings/icon/")
        self.render("account/crop.html", error=None)

    @authenticated
    def post(self):
        if not self.current_user.has_origin_avatar():
            self.redirect("/settings/icon/")

        coords = self.get_argument("coords")
        if not crop_icon(self.current_user.avatar_filename, coords):
            self.render("account/crop.html", error=152)

        self.redirect("/settings/icon/")
