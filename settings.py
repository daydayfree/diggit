# -*- coding: utf-8 -*-

import os.path

# mongodb
MONGODB_SETTINGS = {
    'host': '127.0.0.1',
    'port': '11217',
    'max_pool': 300
}

# image
MIDDLE_WIDTH = 225
THUMB_SIZE = (75, 75)
ICON_WIDTH = 50
ICON_BIG_WIDTH = 160

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../static/upload")
ICONS_DIR = os.path.join(os.path.dirname(__file__), "../static/icons")

# pagination
MINI_PAGE_SIZE = 20
MAX_PAGE_SIZE = 5 * MINI_PAGE_SIZE

try:
    from local_settings import *
except:
    pass
