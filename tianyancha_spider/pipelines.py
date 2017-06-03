# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TianyanchaSpiderPipeline(object):
    def __init__(self):
        self.item_cache = {}

    def process_item(self, item, spider):
        key = item['code']
        if key:
            try:
                self.item_cache[key].update(item)
            except KeyError:
                self.item_cache[key] = item
            return self.item_cache[key]
        return item
