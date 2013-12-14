# -*- coding: utf-8 -*-

import os.path
import time
import tornado.web
from base import BaseHandler
from model import User
from util import sha1
from util import icon_crop
from util import Log


class SettingsHandler(BaseHandler):
    @property
    def user_dal(self): return User()

    @tornado.web.authenticated
    def get(self):
        self.render("account/settings.html", error=None)

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        user["name"] = self.get_argument("name", user["name"])
        user["username"] = self.get_argument("username", "")
        user["city"] = self.get_argument("city", "")
        user["link"] = self.get_argument("link", "")
        user["bio"] = self.get_argument("bio", "")
        result = self.user_dal.update_user(user)
        if result:
            self.render("account/settings.html", error=131)
            return
        self.render("account/settings.html", error=130)
        
        
class PasswordHandler(BaseHandler):
    @property
    def user_dal(self):
        return User()

    error_message = {
        "140": "密码修改成功。",
        "141": "原始密码填写错误。",
        "142": "新密码不能为空。",
        "143": "密码修改出错，请稍后再试。"
    }

    @tornado.web.authenticated
    def get(self):
        self.render("account/pwd.html", error=None)

    @tornado.web.authenticated
    def post(self):
        user = self.current_user
        password = self.get_argument("pwd", "")
        new_pwd = self.get_argument("new_pwd", "")
        if user["password"] != sha1(password):
            self.render("account/pwd.html", error=141)
            return
        if new_pwd == "":
            self.render("account/pwd.html", error=142)
            return
        user["password"] = sha1(new_pwd)
        result = self.user_dal.update_user(user)
        if result:
            self.render("account/pwd.html", error=143)
            return
        current_user = user
        self.render("account/pwd.html", error=140)


class IconHandler(BaseHandler):
    @property
    def user_dal(self):
        return User()

    error_message = {
        "150": "头像修改成功。",
        "151": "请选择头像。",
        "152": "图片格式不支持。",
        "153": "头像修改出错，请稍后再试。"
    }

    image_types = ["jpeg", "png", "gif"]

    @tornado.web.authenticated
    def get(self):
        self.render("account/icon.html", error=None)


    @tornado.web.authenticated
    def post(self):
        if not self.request.files:
            self.render("account/icon.html", error=151)
            return
        files = self.request.files["icon"]
        if len(files) == 0:
            self.render("account/icon.html", error=151)
            return
        if files[0]["content_type"].split("/")[1] not in self.image_types:
            self.render("account/icon.html", error=152)
            return
        image_type = files[0]["content_type"].split("/")[1]
        """TODO头像分片存储"""
        ext = os.path.splitext(files[0]["filename"])[1]
        filepath = "u_%s_%s%s" % (
            self.current_user["_id"], str(int(time.time())), ext)
        file_dir = "%s/%s" % (self.settings["icon_dir"], filepath)
        try:
            writer = open(file_dir, "wb")
            writer.write(files[0]["body"])
            writer.flush()
            writer.close()
        except Exception, ex:
            Log.error(ex)
            self.render("account/icon.html", error=153)
            return
        result = self.user_dal.update_user(self.current_user)
        if result:
            self.render("account/icon.html", error=153)
            return
        file_dir = file_dir.split("/icons_tmp/")[1]
        self.render("account/crop.html", error=None, file_path=file_dir)


class CropIconHandler(BaseHandler):
    @property
    def user_dal(self):
        return User()

    error_message = {
        "150": "头像设置成功。",
        "152": "头像设置出错，重新裁剪试试。"
    }

    @tornado.web.authenticated
    def get(self):
        if "file_path" not in self.request.arguments:
            self.redirect("/settings/icon")
            return
        file_path = self.get_argument("file_path", "")
        if file_path == "":
            self.redirect("/settings/icon")
            return
        file_path = file_path.split("/icons_tmp/")[1]
        self.render("account/crop.html", error=None, file_path=file_path)


    @tornado.web.authenticated
    def post(self):
        coords = self.get_argument("coords")
        file_path = self.get_argument("file_path")
        tmp = "%s/%s" % (self.settings["icon_dir"], file_path)
        response = icon_crop(self.current_user["_id"], tmp, coords)
        if not response["status"]:
            self.render("account/crop.html", error=152, file_path=file_path)
            return
        photo_path = response["photo_path"].split("/icons/")[1]
        middle_path = response["middle_path"].split("/icons/")[1]
        user = self.current_user
        user["photo_url"] = photo_path
        user["middle_photo_url"] = middle_path
        result = self.user_dal.update_user(user)
        if result:
            self.render("account/crop.html", error=152, file_path=file_path)
            return
        self.redirect("/settings/icon")
