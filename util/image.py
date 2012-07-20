# -*- coding: utf-8 -*-

import os
import time

from PIL import Image
from util import Log
from util import get_uuid
from settings import UPLOAD_DIR, MIDDLE_WIDTH, THUMB_SIZE, ICONS_DIR, ICON_BIG_WIDTH, ICON_WIDTH


def upload_crop(image_path, ext):
    response = {}
    pin_width = 0
    pin_height = 0
    if not os.path.exists(image_path):
        response["status"] = True
        response["message"] = "Not found: %s" % image_path
        return response

    image_ext = ext[1:].upper()
    if image_ext == "JPG": image_ext = "JPEG"

    store_dir = _get_image_dir(UPLOAD_DIR)
    base_name = get_uuid()
    source_name = "%s_source%s" % (base_name, ext)
    source_path = os.path.join(store_dir, source_name)
    thumb_name = "%s_thumb%s" % (base_name, ext)
    thumb_path = os.path.join(store_dir, thumb_name)
    middle_name = "%s_mid%s" % (base_name, ext)
    middle_path = os.path.join(store_dir, middle_name)

    # source
    try:
        os.rename(image_path, source_path)
    except Exception:
        Log.error("Save source error: %s" % image_path)
        response["status"] = False
        response["message"] = "Save source error: %s" % image_path
        return response

    img = Image.open(source_path)
    # middle
    dest_width = MIDDLE_WIDTH
    width, height = img.size
    if width < dest_width or height < dest_width:
        response["status"] = False
        response["message"] = "Image size too small"
        return response
    dest_height = int(float(dest_width) * float(height) / float(width))
    img_mid = img.resize((dest_width, dest_height), Image.ANTIALIAS)
    img_mid.save(middle_path, image_ext, quality=150)

    pin_width, pin_height = (dest_width, dest_height)

    # thumb
    dest_width, dest_height = THUMB_SIZE
    left, upper, right, lowwer = 0, 0, dest_width, dest_height
    crop_width, crop_height = dest_width, dest_height
    if float(dest_width)/float(dest_height) < float(width)/float(height):
        crop_height = height
        crop_width = int(height * (float(dest_width) / float(dest_height)))
        left = int((width - crop_width) / 2)
        right = left + crop_width
        lowwer = height
    else:
        crop_width = width
        crop_height = int(width * (float(dest_height) / float(dest_width)))
        upper = int((height - crop_height) / 2)
        lowwer = upper + crop_height
        right = width

    box = (left, upper, right, lowwer)
    img_thumb = img.crop(box)
    img_thumb = img_thumb.resize((dest_width, dest_height), Image.ANTIALIAS)
    img_thumb.save(thumb_path, image_ext, quality=150)

    response["status"] = True
    response["source_path"] = source_path
    response["thumb_path"] = thumb_path
    response["middle_path"] = middle_path
    response["height"] = pin_height
    response["width"] = pin_width
    return response


def icon_crop(user_id, icon_path, coords):
    response = {}
    if not os.path.exists(icon_path):
        response["status"] = False
        response["message"] = "Not Found: %s" % icon_path
        return response

    image_path, ext = os.path.splitext(icon_path)
    store_dir = _get_image_dir(ICONS_DIR)
    thumb_name = "u%s%s%s" % (user_id, str(int(time.time())), ext)
    thumb_path = os.path.join(store_dir, thumb_name)

    middle_name = "u%s%sb%s" % (user_id, str(int(time.time())), ext)
    middle_path = os.path.join(store_dir, middle_name)

    img = Image.open(icon_path)
    left, top, width, height = tuple([int(i) for i in coords.split("|")])
    box = (left, top, left+width, top+height)
    img_thumb = img.crop(box)

    big_size = (ICON_BIG_WIDTH, ICON_BIG_WIDTH)
    img_thumb = img_thumb.resize(big_size, Image.ANTIALIAS)
    img_thumb.save(middle_path, quality=150)
    
    thumb_size = (ICON_WIDTH, ICON_WIDTH)
    img_thumb = img_thumb.resize(thumb_size, Image.ANTIALIAS)
    img_thumb.save(thumb_path, quality=150)

    try:
        os.remove(icon_path)
    except Exception, ex:
        Log.info(ex)

    response["status"] = True
    response["photo_path"] = thumb_path
    response["middle_path"] = middle_path
    return response


def _get_image_dir(holder):
    year, month, day = \
        time.strftime('%Y-%m-%d', time.localtime(time.time())).split("-")
    path = os.path.join(holder, year)
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, month)
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, day)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def _get_unique_path(path, name):
    """判断路径是否存在，存在则文件名添加时间戳。"""
    tmp = os.path.join(path, name)
    if os.path.exists(tmp):
        name = "%s%s" % (str(int(time.time())), name)
    return name
