# -*- coding: utf-8 -*-

import uuid
import hashlib
import binascii
import logging as Log

def encrypt(key):
    hash = hashlib.sha1()
    hash.update(key)
    return hash.hexdigest()


def get_uuid():
    return binascii.b2a_hex(uuid.uuid4().bytes)
