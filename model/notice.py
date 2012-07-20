#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename: model/notice.py

from model import Model

class Notice(Model):
    """
    1.Someone follow you
    2.Someone comment your photo or blog or album
    3.Someone like your photo or blog or album
    """
    table = "notices"

    def save(self, notice):
        return self.insert(notice)


    def get_notices(self, user_id, offset=0, limit=10):
        parameters = {"subscriber_id": user_id}
        return self.query(parameters, offset=offset, limit=limit)


    def read_notice(self, notice_id):
        pass

    def remove_notice(self, user_id, subscriber_id, notice_type):
        parameters = {}
        parameters["user_id"] = user_id
        parameters["subscriber_id"] = subscriber_id
        parameters["notice_type"] = notice_type
        self.remove(parameters)

