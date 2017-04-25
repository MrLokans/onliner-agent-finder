#!/usr/bin/env python

import logging

from scrapy.crawler import CrawlerProcess

from spider.apartment_spider import OnlinerApartmentSpider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


OUTPUT_FILE = 'bulletins.json'
OUPTUT_FORMAT = OUTPUT_FILE.split('.')[-1]


if __name__ == '__main__':
    overriden_settings = {
        'FEED_FORMAT': OUPTUT_FORMAT,
        'FEED_URI': OUTPUT_FILE,
        'SPIDER_LOADER_WARN_ONLY': True,
        'LOG_LEVEL': 'INFO',
    }
    process = CrawlerProcess(overriden_settings)

    process.crawl(OnlinerApartmentSpider)
    process.start()
