# -*- coding: utf-8 -*-

BOT_NAME = 'tianyancha_spider'

SPIDER_MODULES = ['tianyancha_spider.spiders']
NEWSPIDER_MODULE = 'tianyancha_spider.spiders'

USER_AGENT = 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)'

ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Host': 'www.tianyancha.com',
    'Referer': 'http://antirobot.tianyancha.com/captcha/verify?'
               'return_url=http://www.tianyancha.com/search/'
               'abc/11',
}

DOWNLOADER_MIDDLEWARES = {
    'tianyancha_spider.middlewares.CustomDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
   'tianyancha_spider.pipelines.TianyanchaSpiderPipeline': 300,
}

FEED_EXPORTERS = {
    'json': 'tianyancha_spider.item_exporters.UnicodeJsonItemExporter',
    'jl': 'tianyancha_spider.item_exporters.UnicodeJsonLinesItemExporter',

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
