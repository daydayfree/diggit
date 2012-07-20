#!/usr/bin/env python
#-*- coding: utf-8 -*-

from model import Model

class Category(Model):
    table = "categories"

    def save(self):
        cates = ('旅行', '艺术', '建筑', '人物', '摄影', '电影/音乐', '生活', 
                 '汽车', 'DIY', '创意/设计', '萌宠', '美食', '家居', '手绘/插画',
                 '美女', '儿童', '自然', '健康', '服饰/街拍', '婚礼', '体育',
                 '科技', '海报', '产品', '3C数码', '趣味', '妆发', '手工/玩物',
                 '男人', '动漫')
        for cate in cates:
            item = {'_id': self.get_id(), 'name': cate}
            self.insert(item)

    def get_all(self):
        result = self.query(None, 0, 100)
        for item in result:
            item["_id"] = int(item["_id"])
        return result
