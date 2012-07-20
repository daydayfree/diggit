# -*- coding:utf-8 -*-

import os.path
import tornado.web
import handler
import module

from tornado.options import define, options

define('port', default=8888, help='run on the given port', type=int)
define('upload_url', '/upload/')

define('weibo_consumer_key', default='')
define('weibo_consumer_secret', default='')
define('qq_consumer_key', default='')
define('qq_consumer_secret', default='')
define('renren_key', default='')
define('renren_secret', default='')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', handler.IndexHandler),
            (r'/join', handler.JoinHandler),
            (r'/login', handler.LoginHandler),
            (r'/logout', handler.LogoutHandler),
            (r'/open/google', handler.GoogleLoginHandler),
            (r'/open/weibo', handler.WeiboLoginHandler),
            (r'/open/qq', handler.QQLoginHandler),
            (r'/open/renren', handler.RenrenLoginHandler),
            (r'/logout', handler.LogoutHandler),
            (r'/upload', handler.UploadHandler),
            (r'/upload_private', handler.PrivateUploadHandler),
            (r'/user/(\d+)', handler.UserHandler),
            (r'/user/(\d+)/do_follow', handler.FollowHandler),
            (r'/item/(\d+)', handler.ItemHandler),
            (r'/item/(\d+)/do_fav', handler.FavHandler),
            (r'/comment', handler.CommentHandler),
            (r'/settings', handler.SettingsHandler),
            (r'/settings/pwd', handler.PasswordHandler),
            (r'/settings/icon', handler.IconHandler),
            (r'/settings/crop', handler.CropIconHandler),
            (r'/notice', handler.NoticeHandler),
            (r'/user/(\d+)/followers', handler.FollowerHandler),
            (r'/user/(\d+)/friends', handler.FriendHandler),
            (r'/users', handler.UsersHandler),
            (r'/cmtdel', handler.DeleteCommentHandler),
            (r'/ajax/pubu', handler.AjaxHandler),
            (r'/ajax/re', handler.AjaxRelationHandler),
            (r'/ajax/likers', handler.AjaxEntryLikers),
            (r'/ajax/tops', handler.AjaxUserTopsHandler),
            (r'/about', handler.AboutHandler),
            (r'/about/help', handler.HelpHanlder),
            (r'/about/term', handler.TermHandler),
            (r'/a/comment/new', handler.AjaxCommentHandler),
            (r'/all', handler.CategoryHandler),
            (r'/search', handler.SearchHandler),
        ]
        ui_modules = {
            'Account': module.AccountModule,
            'Notice': module.NoticeModule,
            'Entry': module.EntryModule,
            'UserBoard': module.UserBoardModule,
            'UserProfile': module.UserProfileModule,
            'Person': module.PersonModule,
            'Pager': module.PagerModule,
            'Comment': module.CommentModule,
            'Header': module.HeaderModule,
            'CategoriesBar': module.CategoriesBarModule,
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
