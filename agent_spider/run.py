#!/usr/bin/env python

import argparse
import logging

from scrapy.crawler import CrawlerProcess

from agent_spider.apartment_spider import OnlinerApartmentSpider
from agent_spider import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging\
    .getLogger('urllib3.connectionpool')\
    .setLevel(logging.WARNING)
logging.getLogger('scrapy.*').setLevel(logging.INFO)


DEFAULT_OUTPUT_FILE = 'bulletins.json'


def read_default_settings():
    """
    Reads spider settings and returns
    dictionary of settings.
    """
    return {s: getattr(settings, s)
            for s in dir(settings)
            if s.isupper()}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file',
                        default=DEFAULT_OUTPUT_FILE)
    parser.add_argument('-u', '--url-file',
                        help='File with list of URLs to start scrapping from.',
                        default=None)
    parser.add_argument('--use-cache',
                        help='Whether to use URL cache for spider.',
                        action='store_true',
                        default=False)
    return parser.parse_args()


def main():
    args = parse_args()
    spider_settings = read_default_settings()
    overridden_settings = {
        'FEED_FORMAT': args.output_file.split('.')[-1],
        'FEED_URI': args.output_file,
        'SPIDER_LOADER_WARN_ONLY': True,
        'LOG_LEVEL': 'INFO',
    }
    spider_settings.update(overridden_settings)
    process = CrawlerProcess(spider_settings)

    process.crawl(OnlinerApartmentSpider,
                  url_file=args.url_file,
                  use_cache=args.use_cache)
    process.start()


if __name__ == '__main__':
    main()
