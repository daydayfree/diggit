# -*- coding: utf-8 -*-

import pytest
from model.user import User


class TestUser(object):

    def test_new(self):
        name = 'unittest1'
        email = 'unitest1@gmail.com'
        city = 'Beijing'
        blog = 'http://daydayfree.github.io'
        intro = 'I am a unittest!'
        uid = 'unittest1'
        new = User.new(name, email, city, blog, intro, uid)
        assert new
        assert new.name == name
        assert new.email == email
        assert new.city == city
        assert new.blog == blog
        assert new.intro == new.intro
        assert new.uid == uid

    def test_update(self):
        uid = 'unittest1'
        user = User.get_by_uid(uid)
        assert user
        intro = 'I am a unittest (modified)'
        new = user.update(intro=intro)
        assert new
        assert new.intro == intro


if __name__ == '__main__':
    pytest.main()
