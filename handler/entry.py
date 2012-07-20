# -*- coding: utf-8 -*-

import os.path
import datetime
import tornado.web
from base import BaseHandler
from util import Log, Pager
from util import upload_crop
from model import Entry, Fav, Comment, Flag, Relation, User, Category
from search import seg_txt_search

class UploadHandler(BaseHandler):
    @property
    def entry_dal(self): return Entry()

    @property
    def user_dal(self): return User()

    @tornado.web.authenticated
    def get(self):
        self.render("upload.html")

    """
    保存图片信息，更新用户上传图片数。
    """
    def post(self):
        user_id = self.get_argument("uid", None)
        title = self.get_argument("title", "")
        link = self.get_argument("link", "")
        profile = self.get_argument("profile", True)
        tags = self.get_argument("tags", "").split(" ")
        description = self.get_argument("description", "")
        image_path = self.get_argument("Filedata.path", None)
        image_name = self.get_argument("Filedata.name", None)
        image_md5 = self.get_argument("Filedata.md5", None)
        image_size = self.get_argument("Filedata.size", None)
        categories = self.get_argument("categories", None)
        
        if not user_id: return
        user_id = int(user_id)
        if not image_path: return
        
        name, ext = os.path.splitext(image_name)
        response = upload_crop(image_path, ext)
        if not response["status"]: return

        source_path = response["source_path"].split("/upload/")[1]
        thumb_path = response["thumb_path"].split("/upload/")[1]
        middle_path = response["middle_path"].split("/upload/")[1]
        width = response["width"]
        height = response["height"]
        
        entry = self.entry_dal.template()
        entry["user_id"] = user_id
        entry["user"] = self.entry_dal.dbref("users", user_id)
        entry["title"] = title
        entry["link"] = link
        entry["profile"] = profile
        entry["tags"] = tags
        entry["description"] = description
        entry["source"] = source_path
        entry["thumb"] = thumb_path
        entry["middle"] = middle_path
        entry["height"] = height
        entry["width"] = width
        entry["md5"] = image_md5
        entry["size"] = image_size

        if categories:
            entry["categories"] = [int(item.strip()) 
                                   for item in categories.split(",") 
                                   if item.strip()]

        if title:
            title = title.encode("utf-8", "ignore")
            keywords = [seg for seg in seg_txt_search(title) if len(seg) > 1]
            if len(tags) and tags[0]:
                keywords = keywords + tags
            entry["_keywords"] = keywords

        try:
            self.entry_dal.save(entry)
            self.user_dal.update_entries_count(user_id)
        except Exception, ex:
            Log.error(ex)


class ItemHandler(BaseHandler):
    _page_size = 10

    @property
    def entry_dal(self): return Entry()

    @property
    def fav_dal(self): return Fav()
    
    @property
    def relation_dal(self): return Relation()

    @property
    def user_dal(self): return User()

    def get(self, entry_id):
        pager = None
        page_index = self.get_argument("p", "1")
        page_index = int(page_index)
        if page_index < 1: page_index = 1
        entry_id = int(entry_id)
        entry = self.entry_dal.get_entry(entry_id)
        if not entry:
            self.redirect("/404")
            return

        user = entry["user"]
        user["top_entries"] = self.user_dal.get_top_entries(entry["user_id"])
        user["primary"] = self.entry_dal.get_primary_entries(user["_id"], entry["published"])

        faved = False
        if self.current_user:
            faved = self.fav_dal.get_faved_it(
                self.current_user["_id"], entry_id)

        followed = False
        if self.current_user:
            _tmp = self.relation_dal.get_relation(
                self.current_user["_id"], entry["user_id"])
            if _tmp: followed = True
        
        comments = None
        total = self.entry_dal.get_comments_count(entry_id)
        if total > 0:
            offset = (page_index - 1) * self._page_size
            url = "/item/%d" % entry_id
            comments = self.entry_dal.get_comments(
                entry_id, offset=offset, limit=self._page_size)
            if total > self._page_size:
                pager = Pager(self._page_size, total, page_index, url)

        self.render("item.html", entry=entry, comments=comments, 
                    pager=pager, faved=faved, user=user,
                    followed=followed)


"""
保存用户喜欢信息，更新用户喜欢数。
"""
class FavHandler(BaseHandler):
    @property
    def fav_dal(self): return Fav()

    @property
    def user_dal(self): return User()

    @property
    def entry_dal(self): return Entry()

    @tornado.web.authenticated
    def post(self, entry_id):
        if not entry_id or entry_id == "":
            self.write("error")
            return
        user_id = int(self.current_user["_id"])
        entry_id = int(entry_id)
        faved = self.fav_dal.get_faved_it(user_id, entry_id)
        if not faved:
            fav = {
                "_id": self.fav_dal.get_id(),
                "user_id": user_id,
                "user": self.fav_dal.dbref("users", user_id),
                "entry_id": entry_id,
                "entry": self.fav_dal.dbref("entries", entry_id),
                "published": datetime.datetime.now()
            }
            self.fav_dal.save(fav)
            self.user_dal.update_likes_count(user_id)
            self.entry_dal.update_likes_count(entry_id)
            self.write("true")
        else:
            parameters = {"user_id": user_id, "entry_id": entry_id}
            self.fav_dal.remove(parameters)
            self.user_dal.update_likes_count(user_id, -1)
            self.entry_dal.update_likes_count(entry_id, -1)
            self.write("false")
        

"""
保存评论信息，更新图片评论数。
"""
class CommentHandler(BaseHandler):
    @property
    def comment_dal(self): return Comment()

    @property
    def entry_dal(self): return Entry()

    @tornado.web.authenticated
    def post(self):
        user_id = self.current_user["_id"]
        entry_id = self.get_argument("iid", "")
        content = self.get_argument("content", "")
        
        entry_id = int(entry_id)
        comment = {
            "_id": self.comment_dal.get_id(),
            "user_id": user_id,
            "user": self.comment_dal.dbref("users", user_id), 
            "entry_id": entry_id,
            "entry": self.comment_dal.dbref("entries", entry_id),
            "content": content,
            "published": datetime.datetime.now()
        }
        self.comment_dal.save(comment)
        self.entry_dal.update_comments_count(entry_id)
        self.redirect("/item/%s" % entry_id)


class FlagHandler(BaseHandler):
    @property
    def model(self): return Flag()

    @tornado.web.authenticated
    def post(self):
        user_id = self.current_user["_id"]
        image_id = self.get_argument("iid", None)
        reason = self.get_argument("reason", "")
        if not image_id: return
        # save
        user_id = int(user_id)
        image_id = int(image_id)
        comment = {
            "_id": self.model.get_id(),
            "user_id": user_id,
            "user": self.model.dbref("users", user_id),
            "entry_id": image_id,
            "entry": self.model.dbref("entries", image_id),
            "reason": reason,
            "published": datetime.datetime.now()
        }
        self.model.insert(comment)
        self.write("success")


class DeleteCommentHandler(tornado.web.RequestHandler):
    @property
    def comment_dal(self): return Comment()

    @property
    def entry_dal(self): return Entry()

    def get(self):
        id = self.get_argument("id", None)
        tweetid = self.get_argument("tweetid", None)
        if not (id and tweetid):
            self.write("error")
            return
        parameters = {"_id": int(id)}
        self.comment_dal.remove(parameters)
        self.entry_dal.update_comments_count(int(tweetid), -1)
        self.write("ok")


class PrivateUploadHandler(BaseHandler):
    @property
    def category_dal(self): return Category()

    @tornado.web.authenticated
    def get(self):
        categories = self.category_dal.get_all()
        self.render("upload_private.html", categories=categories)
