# -*- coding: utf-8 -*-

import os

from tools.factory import add_or_get_user
from framework import DiggitTestCase
from model.photo import Photo


class DiggitPhotoTestCase(DiggitTestCase):

    def test_can_add_a_new_photo(self):
        user = add_or_get_user('unittest-user1')

        text = 'Hello World!'
        kinds = ['1000', '1001']
        tags = ['Hello', 'World']

        path = os.path.join(os.path.dirname(__file__), 'img/photo.jpg')
        with open(path, 'rb') as f:
            photo = Photo.new(text, kinds, tags, user.id, f.read())

        assert photo
        assert photo.text == text
        assert photo.author
        assert photo.author.id == user.id
        for kind in kinds:
            assert kind in photo.kinds
        for tag in tags:
            assert tag in photo.tags

