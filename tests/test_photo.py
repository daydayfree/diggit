# -*- coding: utf-8 -*-

from framework import DiggitTestCase
from model.photo import Photo
from model.user import User


class DiggitPhotoTestCase(DiggitTestCase):

    def test_can_add_a_new_photo(self):
        name = 'unittest1'
        email = 'unittest1@gmail.com'
        city = 'Beijing'
        blog = 'http://daydayfree.github.io'
        intro = 'I am a unittest!'
        uid = 'unittest2'
        user = User.new(name, email, city, blog, intro, uid)

        text = 'Hello World!'
        height = 400
        width = 220
        kinds = ['1000', '1001']
        tags = ['Hello', 'World']
        author_id = user.id
        photo = Photo.new(text, height, width, kinds, tags, author_id)

        assert photo
        assert photo.text == text
        assert photo.author
        assert photo.author.id == user.id
        for kind in kinds:
            assert kind in photo.kinds
        for tag in tags:
            assert tag in photo.tags

