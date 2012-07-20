#!/usr/bin/env python
#-*- coding: utf-8 -*-

from entry import Entry
from user import User
from search import seg_txt_search

class SearchEngine(object):
    @property
    def entries_dal(self): return Entry()

    def search_entries(self, q, offset=0, limit=10):
        if not q: return None
        if isinstance(q, unicode):
            q = q.encode("utf-8")
        keywords = [seg 
                    for seg in seg_txt_search(q)
                    if len(seg) > 1]
        params = {"_keywords": {"$all": keywords}}
        return self.entries_dal.query(params, offset, limit)

    def search_entries_count(self, q):
        if not q: return 0
        if isinstance(q, unicode):
            q = q.encode("utf-8")
        keywords = [seg 
                    for seg in seg_txt_search(q)
                    if len(seg) > 1]
        params = {"_keywords": {"$all": keywords}}
        return self.entries_dal.get_count(params)
