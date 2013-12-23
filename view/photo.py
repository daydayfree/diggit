# -*- coding: utf-8 -*-

import os.path
import datetime
import tornado.web

from base import BaseHandler
from utils.pager import Pager
from utils.image import upload_crop
from model.user import User
from model.photo import Photo


class UploadHandler(BaseHandler):

    def post(self):
        pass
