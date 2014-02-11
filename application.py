# -*- coding:utf-8 -*-

import os
import tornado.web
from tornado.web import url
from tornado.options import define, options

from module import (
    AccountModule, NoticeModule, EntryModule, UserBoardModule,
    UserProfileModule, PersonModule, PagerModule, CommentModule,
    HeaderModule, CategoriesBarModule
)

from view.index import IndexHandler
from view.login import JoinHandler, LoginHandler, LogoutHandler
from view.about import AboutHandler, HelpHandler, TeamHandler
from view.account import (
    SettingsHandler, PasswordHandler, IconHandler,
    CropIconHandler
)
from view.photo import UploadHandler
from view.j.photo import IndexPhotoHandler
from view import ImageRenderHandler
from view.user import UserHandler
from view.j.fav import FavHandler


define('port', default=9800, help='run on the given port', type=int)
define('weibo_consumer_key', default='')
define('weibo_consumer_secret', default='')
define('qq_consumer_key', default='')
define('qq_consumer_secret', default='')
define('renren_key', default='')
define('renren_secret', default='')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/join/', JoinHandler),
            (r'/login/', LoginHandler),
            (r'/logout/', LogoutHandler),
            (r'/settings/', SettingsHandler),
            (r'/settings/pwd/', PasswordHandler),
            (r'/settings/icon/', IconHandler),
            (r'/settings/crop/', CropIconHandler),
            #(r'/open/google', GoogleLoginHandler),
            #(r'/open/weibo', WeiboLoginHandler),
            #(r'/open/qq', QQLoginHandler),
            #(r'/open/renren', RenrenLoginHandler),
            #(r'/logout', LogoutHandler),
            (r'/upload/', UploadHandler),
            url(r'/image/(?P<category>\w+)/(?P<filename>\w+\.jpg)', ImageRenderHandler, name='image_render'),
            (r'/user/(\w+)/', UserHandler),
            #(r'/user/(\d+)/do_follow', FollowHandler),
            #(r'/item/(\d+)', ItemHandler),
            (r'/j/do_fav', FavHandler),
            #(r'/comment', CommentHandler),
            #(r'/settings', SettingsHandler),
            #(r'/settings/pwd', PasswordHandler),
            #(r'/settings/icon', IconHandler),
            #(r'/settings/crop', CropIconHandler),
            #(r'/notice', NoticeHandler),
            #(r'/user/(\d+)/followers', FollowerHandler),
            #(r'/user/(\d+)/friends', FriendHandler),
            #(r'/users', UsersHandler),
            #(r'/cmtdel', DeleteCommentHandler),
            (r'/j/photos/', IndexPhotoHandler),
            #(r'/ajax/re', AjaxRelationHandler),
            #(r'/ajax/likers', AjaxEntryLikerHandler),
            #(r'/ajax/tops', AjaxUserTopsHandler),
            #(r'/about', AboutHandler),
            #(r'/about/help', HelpHandler),
            #(r'/about/team', TeamHandler),
            #(r'/a/comment/new', AjaxCommentHandler),
            #(r'/all', CategoryHandler),
            #(r'/search', SearchHandler),
        ]
        ui_modules = {
            'Account': AccountModule,
            'Notice': NoticeModule,
            'Entry': EntryModule,
            'UserBoard': UserBoardModule,
            'UserProfile': UserProfileModule,
            'Person': PersonModule,
            'Pager': PagerModule,
            'Comment': CommentModule,
            'Header': HeaderModule,
            'CategoriesBar': CategoriesBarModule,
        }
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
            cookie_secret='11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
            diggit_title='Diggit',
            login_url='/login',
            autoescape=None,
            ui_modules=ui_modules,
            weibo_consumer_key=options.weibo_consumer_key,
            weibo_consumer_secret=options.weibo_consumer_secret,
            qq_consumer_key=options.qq_consumer_key,
            qq_consumer_secret=options.qq_consumer_secret,
            renren_key=options.renren_key,
            renren_secret=options.renren_secret,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


application = Application()
