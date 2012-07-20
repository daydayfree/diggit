# -*- coding: utf-8 -*-

import datetime
import tornado.web

from base import BaseHandler
from util import Log, Pager
from model import Relation, User, Entry


class UserHandler(BaseHandler):

    @property
    def user_dal(self): return User()

    @property
    def entry_dal(self): return Entry()
    
    @property
    def relation_dal(self): return Relation()

    def get(self, user_id):
        filter = self.get_argument("filter", "-1")
        p = int(self.get_argument("p", "1"))
        user = self.user_dal.get(int(user_id))
        if not user:
            self.redirect("/404")
            return

        followed = False
        if self.current_user:
            tmp = self.relation_dal.get_relation(
                self.current_user["_id"], user_id)
            if tmp: followed = True
        self.render("user.html", user=user, followed=followed, 
                    p=p, filter=filter)


class UsersHandler(BaseHandler):
    page_size = 2
    @property
    def user_dal(self): return User()

    def get(self):
        page = int(self.get_argument("p", "1"))
        offset = (page - 1) * self.page_size
        
        total = self.user_dal.get_users_count()
        users = self.user_dal.get_users(offset=offset, limit=self.page_size)
        pager = Pager(self.page_size, total, page, url="/users")
        self.render("users.html", users=users, pager=pager)

"""
保存用户关注信息，更新用户关注数和粉丝数。
"""
class FollowHandler(BaseHandler):
    @property
    def relation_dal(self): return Relation()

    @property
    def user_dal(self): return User()

    @tornado.web.authenticated
    def post(self, user_id):
        follower_id = self.current_user["_id"]
        user_id = int(user_id)
        follower_id = int(follower_id)
        _tmp = self.relation_dal.get_relation(follower_id, user_id)
        if _tmp:
            self.relation_dal.remove_relation(follower_id, user_id)
            self.user_dal.update_friends_count(follower_id, -1)
            self.user_dal.update_followers_count(user_id, -1)
            self.write("false")
            return
        relation = {
            "_id": self.relation_dal.get_id(),
            "follower_id": follower_id,
            "follower": self.relation_dal.dbref("users", follower_id),
            "user_id": user_id,
            "user": self.relation_dal.dbref("users", user_id),
            "published": datetime.datetime.now()
        }
        relation_id = self.relation_dal.save(relation)
        self.user_dal.update_friends_count(follower_id)
        self.user_dal.update_followers_count(user_id)
        if not relation_id:
            self.write("false")
            return
        self.write("true")


class FollowerHandler(BaseHandler):

    @property
    def relation(self): return Relation()

    @property
    def user_dal(self): return User()

    def get(self, user_id):
        args = {'user': None, 'followed': False, 'p': 1}
        args['p'] = int(self.get_argument("p", "1"))

        user_id = int(user_id)
        user = self.user_dal.get(user_id)
        if not user:
            self.redirect("/")
            return

        args["user"] = user
        if self.current_user:
            tmp = self.relation.get_relation(
                self.current_user["_id"], user_id)
            if tmp: 
                args['followed'] = True

        self.render("followers.html", **args)


class FriendHandler(BaseHandler):
    @property
    def relation_dal(self): return Relation()

    @property
    def user_dal(self): return User()
    
    def get(self, user_id):
        p = int(self.get_argument("p", "1"))
        user_id = int(user_id)
        user = self.user_dal.get(user_id)
        followed = False
        if self.current_user:
            _tmp = self.relation_dal.get_relation(
                self.current_user["_id"], user_id)
            if _tmp: followed = True
        
        self.render("friends.html", user=user, followed=followed, 
                    p=p)
