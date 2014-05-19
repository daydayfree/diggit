# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
from application import application


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()
