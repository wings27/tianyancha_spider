# -*- coding: utf-8 -*-

import scrapy


class TianyanchaSpiderItem(scrapy.Item):
    status = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    download_timeout = scrapy.Field()
    depth = scrapy.Field()

    share_holder = scrapy.Field()
    patent_content = scrapy.Field()
    lawsuit_content = scrapy.Field()
