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

        def bs_extract_holders(bs):
            holders = bs.find('div', {'ng-if': 'dataItemCount.holderCount>0'})
            return holders.decode_contents(formatter="html")

        def bs_extract_lawsuit(bs):
            holders = bs.find('div', {'ng-if': 'dataItemCount.lawsuitCount>0'})
            return holders.decode_contents(formatter="html")

        def bs_extract_patent(bs):
            holders = bs.find('div', {'ng-if': 'dataItemCount.patentCount>0'})
            return holders.decode_contents(formatter="html")

        beautiful_soup = BeautifulSoup(response.body, 'html.parser')
        if response.url.startswith('http://www.tianyancha.com/search'):
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
                              dont_filter=True, meta=response.meta)
                yield Request('http://www.tianyancha.com/expanse/patent.json?'
                              'id=%s&ps=1000&pn=1' % company_code,
                              dont_filter=True, meta=response.meta)

        elif response.url.startswith('http://www.tianyancha.com/company'):
            company_code = extract_company_code(response.url)
            holders_content = bs_extract_holders(beautiful_soup)
            lawsuit_content = bs_extract_lawsuit(beautiful_soup)
            patent_content = bs_extract_patent(beautiful_soup)
            yield TianyanchaSpiderItem(code=company_code,
                                       name=response.meta['name'],
                                       status='OK',
                                       holders_content=holders_content,
                                       lawsuit_content=lawsuit_content,
                                       patent_content=patent_content, )
        else:
            # json result
            if response.url.startswith('http://www.tianyancha.com/stock/equityChange.json'):
                equity_change = beautiful_soup.find('pre').text
                yield TianyanchaSpiderItem(code=response.meta['code'],
                                           equity_change=equity_change)
            if response.url.startswith('http://www.tianyancha.com/expanse/patent.json'):
                patent_content = beautiful_soup.find('pre').text
                yield TianyanchaSpiderItem(code=response.meta['code'],
                                           patent_content=patent_content)
            print(response.body)

    # 股本变化情况  http://www.tianyancha.com/stock/equityChange.json?graphId=640320&ps=1000&pn=1
    # 法律诉讼  http://www.tianyancha.com/v2/getlawsuit/NAME.json?page=1&ps=1000
    # 专利  http://www.tianyancha.com/expanse/patent.json?id=640320&pn=1&ps=1000

    def init_urls(self):
        try:
            with open('names.txt', encoding='utf8') as f:
                lines = f.readlines()
                return ((name.strip(), self.base_url % name.strip()) for name in lines)
        except FileNotFoundError:
            pass
