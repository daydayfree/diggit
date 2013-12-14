# -*- coding: utf-8 -*-

import os
import shutil

from settings import PHOTO_PATH


class FileStore(object):

    def __init__(self, domain):
        self.domain = domain

    def path(self, filename, category=None):
        if category:
            return "%s/%s/%s" % (self.domain, category, filename)
        else:
            return "%s/%s" % (self.domain, filename)

    def filepath(self, filename, category=None):
        if filename[:1] in 'xp':
            filename = filename[1:]
        path = self.path(filename, category)
        return os.path.join(PHOTO_PATH, path)

    def load(self, filename, category=None):
        path = self.filepath(filename, category)
        if os.path.exists(path):
            return open(path).read()

    def save(self, filename, content, category=None):
        path = self.filepath(filename, category)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        open(path, 'w').write(content)
        return path

    def delete(self, filename, category=None):
        path = self.filepath(filename, category)
        if os.path.exists(path):
            os.remove(path)
            return True

    def copy(self, orig_filename, new_filename, category=None):
        path = self.filepath(orig_filename, category)
        if self.exists(orig_filename, category):
            new_path = self.filepath(new_filename, category)
            if not os.path.exists(os.path.dirname(new_path)):
                os.makedirs(os.path.dirname(new_path))
            shutil.copyfile(path, new_path)
            return new_path

    def exists(self, filename, category=""):
        path = self.filepath(filename, category)
        return os.path.exists(path)

    def rename(self, old_filename, new_filename, category=None):
        old_path = self.filepath(old_filename, category)
        if self.exists(old_filename, category):
            new_path = self.filepath(new_filename, category)
            if not os.path.exists(os.path.dirname(new_path)):
                os.makedirs(os.path.dirname(new_path))
            if os.path.exists(new_path):
                os.remove(new_path)
            os.rename(old_path, new_path)
            return new_path


fs = FileStore('photo')
