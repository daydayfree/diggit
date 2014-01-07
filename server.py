# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import options
from application import application


if __name__ == '__main__':
    print 'Tornado web server listening at %s' % options.port
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
