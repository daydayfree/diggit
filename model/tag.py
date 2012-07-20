#!/usr/bin/env python

from model import Model

class Tag(Model):
    table = "tags"

    def get_tags(self, offset=0, limit=10):
        result = []
        cursor = self.db.query(self.table, None, "value", offset, limit)
        if cursor and cursor.count():
            result = [item for item in cursor if item["_id"]]
        return result
