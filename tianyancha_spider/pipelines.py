# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TianyanchaSpiderPipeline(object):
    def __init__(self):
        self.item_cache = {}

    def process_item(self, item, spider):
        if item['code']:
            try:
                self.item_cache[item['code']] = self.item_cache[item['code']].update(item)
                return self.item_cache[item['code']]
            except KeyError:
                return item
        return item
