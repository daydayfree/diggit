#!/usr/bin/env python
#-*- coding: utf-8 -*-
#filename: model/message.py

from model import Model

class Message(Model):
    table = "messages"
    
    def get_inbox(self, user_id, offset=0, limit=10):
        pass


    def get_outbox(self, user_id, offset=0, limit=10):
        pass


    def read_message(self, message_id):
        pass


    def get_parent_message(self, message_id):
        pass

