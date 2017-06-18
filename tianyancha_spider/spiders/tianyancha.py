# -*- coding: utf-8 -*-
import json

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from tianyancha_spider.items import TianyanchaSpiderItem


class TianyanchaSpider(scrapy.Spider):
    name = "tianyancha"
    allowed_domains = ["tianyancha.com"]
    base_url = 'http://www.tianyancha.com/search?key=%s'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = self.init_urls()
        self.item_cache = {}

    def start_requests(self):
        for (name, url) in self.start_urls:
            request = Request(url, dont_filter=True, meta={'name': name})
            yield request

    def parse(self, response):
        def extract_company_code(company_link):
            return company_link[len('http://www.tianyancha.com/company/'):]

        beautiful_soup = BeautifulSoup(response.body, 'html.parser')

        qn = beautiful_soup.find('a', class_='query_name')
        name = response.meta['name']
        if not qn:
            return TianyanchaSpiderItem(name=name, status='Not found')
        link = qn['href']
        if link.startswith('http://www.tianyancha.com/company'):
            company_code = extract_company_code(link)
            response.meta.update({'code': company_code})
            yield Request('http://www.tianyancha.com/stock/equityChange.json?'
                          'graphId=%s&ps=1000&pn=1' % company_code,
                          dont_filter=True, meta=response.meta,
                          callback=self.equity_change)
            yield Request('http://www.tianyancha.com/expanse/patent.json?'
                          'id=%s&ps=1000&pn=1' % company_code,
                          dont_filter=True, meta=response.meta,
                          callback=self.patent_content)
            yield Request('http://www.tianyancha.com/v2/getlawsuit'
                          '/%s.json?page=1&ps=1000' % name,
                          dont_filter=True, meta=response.meta,
                          callback=self.lawsuit_content)

    def equity_change(self, response):
        beautiful_soup = BeautifulSoup(response.body, 'html.parser')
        equity_change = beautiful_soup.find('pre').text
        equity_change = json.loads(equity_change)
        response.meta.update({'equity_change': equity_change})
        yield self._update_item_cache(response)

    def patent_content(self, response):
        beautiful_soup = BeautifulSoup(response.body, 'html.parser')
        patent_content = beautiful_soup.find('pre').text
        patent_content = json.loads(patent_content)
        response.meta.update({'patent_content': patent_content})
        yield self._update_item_cache(response)

    def lawsuit_content(self, response):
        beautiful_soup = BeautifulSoup(response.body, 'html.parser')
        lawsuit_content = beautiful_soup.find('pre').text
        lawsuit_content = json.loads(lawsuit_content)
        response.meta.update({'lawsuit_content': lawsuit_content})
        yield self._update_item_cache(response)

    def _update_item_cache(self, response):
        item = TianyanchaSpiderItem(response.meta)
        key = item['code']
        if key:
            try:
                self.item_cache[key].update(item)
            except KeyError:
                self.item_cache[key] = item
        cached_item = self.item_cache[key]
        if all(k in cached_item for k in (
                'equity_change', 'patent_content', 'lawsuit_content')):
            return cached_item

    def init_urls(self):
        try:
            with open('names.txt', encoding='utf8') as f:
                lines = f.readlines()
                return ((name.strip(), self.base_url % name.strip())
                        for name in lines if name.strip())
        except FileNotFoundError:
            pass
