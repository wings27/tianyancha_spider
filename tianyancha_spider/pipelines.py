# -*- coding: utf-8 -*-
from datetime import datetime

from tianyancha_spider.spiders.tianyancha import TianyanchaSpider


class TianyanchaSpiderPipeline(object):
    @staticmethod
    def format_date(date_long: int) -> str:
        return datetime.fromtimestamp(date_long / 1000).strftime('%Y.%m.%d')

    def __init__(self) -> None:
        self.counter = {
            TianyanchaSpider.SHARE_HOLDER: 0,
            TianyanchaSpider.LAWSUIT_CONTENT: 0,
            TianyanchaSpider.PATENT_CONTENT: 0
        }

    def process_item(self, item, spider):
        if TianyanchaSpider.SHARE_HOLDER in item:
            share_holder = item[TianyanchaSpider.SHARE_HOLDER]
            holder_list = share_holder['data']['holderList']
            for (i, elem) in enumerate(holder_list):
                row_num = self.counter[TianyanchaSpider.SHARE_HOLDER] + i
                row_content = (item['name'], elem['name'],
                               elem['proportion'], elem['holdingNum'],
                               self.format_date(elem['publishDate']))
                print('%s: %d: %s' % (TianyanchaSpider.SHARE_HOLDER,
                                      row_num, row_content))
            self.counter[TianyanchaSpider.SHARE_HOLDER] += len(holder_list)
        if TianyanchaSpider.PATENT_CONTENT in item:
            patent_content = item[TianyanchaSpider.PATENT_CONTENT]
            items = patent_content['data']['items']
            for (i, elem) in enumerate(items):
                row_num = self.counter[TianyanchaSpider.PATENT_CONTENT] + i
                row_content = (elem['applicantName'],
                               elem['applicationPublishNum'],
                               elem['applicationPublishTime'],
                               elem['patentName'], elem['patentType'])
                print('%s: %d: %s' % (TianyanchaSpider.PATENT_CONTENT,
                                      row_num, row_content))
            self.counter[TianyanchaSpider.PATENT_CONTENT] += len(items)
        return item
