# -*- coding: utf-8 -*-

import pytest

from model.user import User
from model.photo import Photo


class TestPhoto(object):

    def test_new(self):
        user = User.get_by_uid('test1')
        assert user

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


if __name__ == '__main__':
    pytest.main()
