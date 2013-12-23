# -*- coding:utf-8 -*-

import os
import tornado.web

from tornado.options import define, options

define('port', default=9800, help='run on the given port', type=int)
define('upload_url', '/upload/')

define('weibo_consumer_key', default='')
define('weibo_consumer_secret', default='')
define('qq_consumer_key', default='')
define('qq_consumer_secret', default='')
define('renren_key', default='')
define('renren_secret', default='')

from module import (
    AccountModule, NoticeModule, EntryModule, UserBoardModule,
    UserProfileModule, PersonModule, PagerModule, CommentModule,
    HeaderModule, CategoriesBarModule
)

from view.index import IndexHandler
from view.login import JoinHandler, LoginHandler, LogoutHandler
    #GoogleLoginHandler,
    #WeiboLoginHandler, QQLoginHandler, RenrenLoginHandler,
    #CategoryHandler
#)
#from view.entry import (
#    UploadHandler, PrivateUploadHandler, ItemHandler,
#    FavHandler, CommentHandler, DeleteCommentHandler
#)
#from view.user import (
#    UserHandler, FollowHandler, FollowerHandler, FriendHandler,
#    UsersHandler
#)
#from view.account import (
#    SettingsHandler, PasswordHandler, IconHandler,
#    CropIconHandler
#)
#from view.feed import NoticeHandler
#from view.ajax import (
#    AjaxHandler, AjaxRelationHandler, AjaxEntryLikerHandler, AjaxUserTopsHandler,
#    AjaxCommentHandler
#)
from view.about import AboutHandler, HelpHandler, TeamHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/join', JoinHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            #(r'/open/google', GoogleLoginHandler),
            #(r'/open/weibo', WeiboLoginHandler),
            #(r'/open/qq', QQLoginHandler),
            #(r'/open/renren', RenrenLoginHandler),
            #(r'/logout', LogoutHandler),
            #(r'/upload', UploadHandler),
            #(r'/upload_private', PrivateUploadHandler),
            #(r'/user/(\d+)', UserHandler),
            #(r'/user/(\d+)/do_follow', FollowHandler),
            #(r'/item/(\d+)', ItemHandler),
            #(r'/item/(\d+)/do_fav', FavHandler),
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
            #(r'/ajax/pubu', AjaxHandler),
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
            template_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=False,
            cookie_secret='11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
            diggit_title='Diggit',
            login_url='/login',
            autoescape=None,
            ui_modules=ui_modules,
            upload_url=options.upload_url,
            icon_dir=os.path.join(
                os.path.dirname(__file__), 'static/icons_tmp'),
            weibo_consumer_key=options.weibo_consumer_key,
            weibo_consumer_secret=options.weibo_consumer_secret,
            qq_consumer_key=options.qq_consumer_key,
            qq_consumer_secret=options.qq_consumer_secret,
            renren_key=options.renren_key,
            renren_secret=options.renren_secret,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
