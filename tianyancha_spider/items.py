# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanchaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    status = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    holders_content = scrapy.Field()
    lawsuit_content = scrapy.Field()
    pass
