#!/usr/bin/env python

import argparse
import logging

from scrapy.crawler import CrawlerProcess

from spider.apartment_spider import OnlinerApartmentSpider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEFAULT_OUTPUT_FILE = 'bulletins.json'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file',
                        default=DEFAULT_OUTPUT_FILE)
    return parser.parse_args()


def main():
    args = parse_args()
    overridden_settings = {
        'FEED_FORMAT': args.output_file,
        'FEED_URI': args.output_file.split('.')[-1],
        'SPIDER_LOADER_WARN_ONLY': True,
        'LOG_LEVEL': 'INFO',
    }
    process = CrawlerProcess(overridden_settings)

    process.crawl(OnlinerApartmentSpider)
    process.start()


if __name__ == '__main__':
    main()
