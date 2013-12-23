#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from model.user import User

def add_test_user():
    name = 'test1'
    email = 'test1@gmail.com'
    city = 'Beijing'
    blog = 'http://daydayfree.github.io'
    intro = 'I am a test!'
    uid = 'test1'
    User.new(name, email, city, blog, intro, uid)
    print 'Add test user:uid=%s' % uid


if __name__ == '__main__':
    add_test_user()

