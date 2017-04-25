#!/usr/bin/env python

import logging

from scrapy.crawler import CrawlerProcess

from spider.apartment_spider import OnlinerApartmentSpider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


OUTPUT_FILE = 'bulletins.json'
OUTPUT_FORMAT = OUTPUT_FILE.split('.')[-1]


def main():
    overridden_settings = {
        'FEED_FORMAT': OUTPUT_FORMAT,
        'FEED_URI': OUTPUT_FILE,
        'SPIDER_LOADER_WARN_ONLY': True,
        'LOG_LEVEL': 'INFO',
    }
    process = CrawlerProcess(overridden_settings)

    process.crawl(OnlinerApartmentSpider)
    process.start()


if __name__ == '__main__':
    main()
