# -*- coding:utf-8 -*-

from model.user import User


def add_or_get_user(name):
    user = User.get_by_uid(name)
    if user:
        return user
    email = 'fuyao@gmail.com'
    city = 'Beijing'
    blog = 'http://fuyao.github.io'
    intro = 'I am a unittest!'
    return User.new(name, email, city, blog, intro, name)
