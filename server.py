# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import options
from application import Application


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
