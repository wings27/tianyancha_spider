# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class TianyanchaSpider(scrapy.Spider):
    name = "tianyancha"
    allowed_domains = ["tianyancha.com"]
    base_url = 'http://www.tianyancha.com/search?key=%s'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = self.init_urls()
        print(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        if response.url.startswith('http://www.tianyancha.com/search'):
            bs = BeautifulSoup(response.body, 'html.parser')
            qn = bs.find('a', class_='query_name')
            if not qn:
                return {'state': '暂未收录该公司'}
            link = qn['href']
            yield self.make_requests_from_url(link)
        elif response.url.startswith('http://www.tianyancha.com/company'):
            bs = BeautifulSoup(response.body, 'html.parser')
            print(response.body)

    def init_urls(self):
        try:
            with open('names.txt', encoding='utf8') as f:
                lines = f.readlines()
                return [self.base_url % name.strip() for name in lines]
        except FileNotFoundError:
            pass
