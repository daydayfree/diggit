# -*- coding: utf-8 -*-

from cStringIO import StringIO
from PIL import Image

from corelib.filestore import fs
from corelib.consts import (
    MIDDLE_WIDTH, THUMB_WIDTH, THUMB_HEIGHT, ICON_WIDTH,
    ICON_ORIGIN_WIDTH
)


def crop_photo(filename, content):
    source_path = fs.save(filename, content, 'origin')

    image = Image.open(source_path)
    width, height = image.size

    middle_width = MIDDLE_WIDTH
    if width < middle_width or height < middle_width:
        return False

    middle_height = int(float(middle_width) * float(height) / float(width))
    middle_image = image.resize((middle_width, middle_height), Image.ANTIALIAS)
    middle_path = fs.filepath(filename, 'photo')
    middle_image.save(middle_path, quality=150)

    # thumb
    left, upper, right, lowwer = 0, 0, THUMB_WIDTH, THUMB_HEIGHT
    crop_width, crop_height = THUMB_WIDTH, THUMB_HEIGHT
    if float(THUMB_WIDTH)/float(THUMB_HEIGHT) < float(width)/float(height):
        crop_height = height
        crop_width = int(height * (float(THUMB_WIDTH) / float(THUMB_HEIGHT)))
        left = int((width - crop_width) / 2)
        right = left + crop_width
        lowwer = height
    else:
        crop_width = width
        crop_height = int(width * (float(THUMB_HEIGHT) / float(THUMB_WIDTH)))
        upper = int((height - crop_height) / 2)
        lowwer = upper + crop_height
        right = width

    box = (left, upper, right, lowwer)
    thumb_image = image.crop(box)
    thumb_image = thumb_image.resize((THUMB_WIDTH, THUMB_HEIGHT), Image.ANTIALIAS)
    thumb_path = fs.filepath(filename, 'thumb')
    thumb_image.save(thumb_path, quality=150)

    return middle_width, middle_height


def save_origin_icon(filename, content):
    image = Image.open(StringIO(content))
    width, height = image.size
    if width > 500:
        width = 500
        height = int(height * 500 / float(width))
    if height < 100:
        return False
    i = image.resize((width, height), Image.ANTIALIAS)
    p = fs.filepath(filename, 'origin')
    i.save(p, quality=150)


def crop_icon(filename, coords):
    coords = coords.split(' ')
    if len(coords) != 4:
        return False
    left, top, width, height = map(int, coords)

    source_path = fs.filepath(filename, 'origin')

    image = Image.open(source_path)
    box = (left, top, left+width, top+height)
    origin_image = image.crop(box)

    origin_image = origin_image.resize((ICON_ORIGIN_WIDTH, ICON_ORIGIN_WIDTH),
                                       Image.ANTIALIAS)
    origin_path = fs.filepath(filename, 'photo')
    origin_image.save(origin_path, quality=150)

    thumb_image = origin_image.resize((ICON_WIDTH, ICON_WIDTH), Image.ANTIALIAS)
    thumb_path = fs.filepath(filename, 'thumb')
    thumb_image.save(thumb_path, quality=150)

    fs.delete(filename, 'origin')
    return True
