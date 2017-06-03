# -*- coding: utf-8 -*-
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
        print(self.start_urls)

    def start_requests(self):
        for (name, url) in self.start_urls:
            request = Request(url, dont_filter=True, meta={'name': name})
            yield request

    def parse(self, response):
        def extract_company_code(company_link):
            return company_link[len('http://www.tianyancha.com/company/'):]

        if response.url.startswith('http://www.tianyancha.com/search'):
            bs = BeautifulSoup(response.body, 'html.parser')
            qn = bs.find('a', class_='query_name')
            name = response.meta['name']
            if not qn:
                return TianyanchaSpiderItem(name=name, status='Not found')
            link = qn['href']
            if link.startswith('http://www.tianyancha.com/company'):
                request = Request(link, dont_filter=True, meta=response.meta)
                yield request
        elif response.url.startswith('http://www.tianyancha.com/company'):
            company_code = extract_company_code(response.url)
            bs = BeautifulSoup(response.body, 'html.parser')
            holders = bs.find('div', {'ng-if': 'dataItemCount.holderCount>0'})
            holders_content = holders.decode_contents(formatter="html")
            yield TianyanchaSpiderItem(code=company_code,
                                       name=response.meta['name'],
                                       status='OK',
                                       holders_content=holders_content)

    def init_urls(self):
        try:
            with open('names.txt', encoding='utf8') as f:
                lines = f.readlines()
                return ((name.strip(), self.base_url % name.strip()) for name in lines)
        except FileNotFoundError:
            pass
