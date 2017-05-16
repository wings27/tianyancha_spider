# -*- coding: utf-8 -*-
import scrapy


class TianyanchaSpider(scrapy.Spider):
    name = "tianyancha"
    allowed_domains = ["tianyancha.com"]
    start_urls = ['http://tianyancha.com/']

    def parse(self, response):
        pass
