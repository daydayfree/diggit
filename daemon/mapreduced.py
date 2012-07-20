#!/usr/bin/env python

from bson.code import Code
from bson.dbref import DBRef
from database import Database
from util import Log

class UserMapReduced(object):
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.mongo = Database()
        self.reduce = Code(
            "function(key, values) {"
            "  var result = { entries:0, likes:0, followers:0, friends:0 };"
            "  values.forEach(function(value) {"
            "    if (value.entries !== null) {"
            "      result.entries += value.entries;"
            "    }"
            "    if (value.likes !== null) {"
            "      result.likes += value.likes;"
            "    }"
            "    if (value.followers !== null) {"
            "      result.followers += value.followers;"
            "    }"
            "    if (value.friends !== null) {"
            "      result.friends += value.friends;"
            "    }"
            "  });"
            "  return result;"
            "}")
    
    def _reduce_entries(self):
        map = Code(
            "function() {"
            "  var args = { entries:1, likes:0, followers:0, friends:0 };"
            "  emit(this.user_id, args);"
            "}")
        self.mongo.db["entries"].map_reduce(
            map, self.reduce, out={"reduce" : "user_status"})

    def _reduce_likes(self):
        map = Code(
            "function() {"
            "  var args = { entries:0, likes:1, followers:0, friends:0 };"
            "  emit(this.user_id, args);"
            "}")
        self.mongo.db["favs"].map_reduce(
            map, self.reduce, out={"reduce" : "user_status"})

    def _reduce_followers(self):
        map = Code(
            "function() {"
            "  var args = { entries:0, likes:0, followers:1, friends:0 };"
            "  emit(this.user_id, args);"
            "}")
        self.mongo.db["relations"].map_reduce(
            map, self.reduce, out={"reduce" : "user_status"})

    def _reduce_friends(self):
        map = Code(
            "function() {"
            "  var args = { entries:0, likes:0, followers:0, friends:1 };"
            "  emit(this.follower_id, args);"
            "}")
        self.mongo.db["relations"].map_reduce(
            map, self.reduce, out={"reduce" : "user_status"})

    def _clear_result(self):
        self.mongo.db["user_status"].remove()

    def _save_result(self):
        cursor = self.mongo.db.user_status.find()
        for item in cursor:
            params = {"_id": item["_id"]}
            for k, v in item["value"].items():
                item["value"][k] = int(v)
            user = {"count_info" : item["value"] }
            self.mongo.db.users.update(params, {"$set" : user})
    
    def process(self):
        try:
            self._clear_result()
            self._reduce_entries()
            self._reduce_likes()
            self._reduce_followers()
            self._reduce_friends()
        except Exception, ex:
            Log.error(ex, "mapreduce")
            return
        try:
            self._save_result()
        except Exception, ex:
            Log.error(ex, "mapreduce")
    

class EntryMapReduced(object):
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.mongo = Database()
        self.reduce = Code(
            "function(key, values) {"
            "  var result = { cmts:[], cmtscount:0, favs:[], favscount:0 };"
            "  values.forEach(function(value) {"
            "    if (value.cmts !== null) {"
            "      for(var i=0; i<value.cmts.length; i++) {"
            "        result.cmts.push(value.cmts[i]);"
            "      }"
            "    }"
            "    if (value.cmtscount !== null) {"
            "      result.cmtscount += value.cmtscount;"
            "    }"
            "    if (value.favs !== null) {"
            "      for(var j=0; j<value.favs.length; j++) {"
            "        result.favs.push(value.favs[i]);"
            "      }"
            "    }"
            "    if (value.favscount !== null) {"
            "      result.favscount += value.favscount;"
            "    }"
            "  });"
            "  return result;"
            "}")

    def _clear_result(self):
        self.mongo.db.entries_status.remove()
        
    def _reduce_favers(self):
        map = Code(
            "function() {"
            "  var args = { cmts:[], cmtscount:0, favs:[this.user_id], favscount:1 };"
            "  emit(this.entry_id, args);"
            "}")
        self.mongo.db.favs.map_reduce(
            map, self.reduce, out={"reduce": "entries_status"})
        
    def _reduce_comments(self):
        map = Code(
            "function() {"
            "  var args = { cmts:[this._id], cmtscount:1, favs:[], favscount:0 };"
            "  emit(this.entry_id, args);"
            "}")
        self.mongo.db["comments"].map_reduce(
            map, self.reduce, out={"reduce": "entries_status"})

    def _save_result(self):
        cursor = self.mongo.db.entries_status.find()
        for item in cursor:
            params = {"_id": item["_id"]}
            entry = {
                "cmtscount": item["value"]["cmtscount"],
                "cmts": [],
                "favscount": item["value"]["favscount"],
                "favs": []
            }
            for cmtid in item["value"]["cmts"]:
                entry["cmts"].append(DBRef("comments", cmtid))
            for userid in item["value"]["favs"]:
                entry["favs"].append(DBRef("users", userid))
            self.mongo.db.entries.update(params, {"$set" : entry})

    def process(self):
        try:
            self._clear_result()
            self._reduce_comments()
            self._reduce_favers()
        except Exception, ex:
            Log.error(ex, "mapreduce")
        self._save_result()


class TagsMapReduced(object):
    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.mongo = Database()
        self.map = Code(
            "function() {"
            "  this.tags.forEach("
            "    function(tag) {"
            "      emit(tag, 1);"
            "    }"
            "  )"
            "}"
        )
        self.reduce = Code(
            "function(key, values) {"
            "  var total = 0;"
            "  for (var i=0; i<values.length; i++) {"
            "    total += values[i];"
            "  }"
            "  return total;"
            "}"
        )

    def process(self):
        self.mongo.db.entries.map_reduce(
            self.map, self.reduce, out={"reduce": "tags"})
