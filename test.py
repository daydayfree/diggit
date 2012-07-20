# -*- coding: utf-8 -*-

import time

def timeit(func):
    def warpper():
        start = time.time()
        func()
        print "used:", time.time() - start
    return warpper


def insert():
    from model import User
    mongo = User()
    mongo.insert({"id": 1, "name": "meego"})


def get_id():
    from database import Database
    mongo = Database()
    id = mongo.get_id("user")
    print id["value"]
    

# decorator
def validate_required_parameters(parameters):
    def wrapper(func):
        """parameters"""
        return func
    return wrapper

@validate_required_parameters("meego")
def foo():
    print "I am foo"


def sha1():
    from util import sha1
    print sha1("daydayfree")


def crop():
    import util
    image_path = "/home/meego/Desktop/dd"
    ext = ".jpg"
    response = util.upload_crop(image_path, ext)
    for param in response:
        print response[param]

def icon_crop():
    import util
    icon_path = "/home/meego/Desktop/dd.jpg"
    user_id = 2006
    coords = "200|100|200|200"
    response = util.icon_crop(user_id, icon_path, coords)
    for param in response:
        print response[param]
    


def path_split():
    import util
    file_path = "/home/meego/python/blade/trunk/src/static/header.jpg"
    dir, name, ext = util.path_split(file_path)
    print dir
    print name
    print ext


def log():
    from util import Log
    Log.info("Hello from test.py")


def query():
    from model import Entry
    entry_dal = Entry()
    for i in entry_dal.query(None, "updated"):
        print i


def pager():
    from util import Pager
    pager = Pager(10, 231, 2)
    pager.display()

def main():
    pager()


def categories():
    from model import Category
    category = Category()
    category.save()


def get_all_categories():
    from model import Category
    category = Category()
    for item in category.get_all():
        print item


def segment():
    title = "故事的小黄花,从出生那年就开始飘着"
    from search import seg_title_search
    for s in seg_title_search(title):
        print s

def search():
    from model import SearchEngine
    engine = SearchEngine()
    q = "故事的小黄花"
    print engine.search_entries_count(q)

if __name__ == "__main__":
    search()
