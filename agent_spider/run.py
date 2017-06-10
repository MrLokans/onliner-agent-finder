#!/usr/bin/env python

import argparse
import logging

from scrapy.crawler import CrawlerProcess

from agent_spider.apartment_spider import OnlinerApartmentSpider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging\
    .getLogger('urllib3.connectionpool')\
    .setLevel(logging.WARNING)
logging.getLogger('scrapy.*').setLevel(logging.INFO)


DEFAULT_OUTPUT_FILE = 'bulletins.json'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file',
                        default=DEFAULT_OUTPUT_FILE)
    parser.add_argument('-u', '--url-file',
                        help='File with list of URLs to start scrapping from.',
                        default=None)
    parser.add_argument('-c', '--cache',
                        help='Whether to use URL cache for spider.',
                        default=False,
                        type=bool)
    return parser.parse_args()


def main():
    args = parse_args()
    overridden_settings = {
        'FEED_FORMAT': args.output_file.split('.')[-1],
        'FEED_URI': args.output_file,
        'SPIDER_LOADER_WARN_ONLY': True,
        'LOG_LEVEL': 'INFO',
    }
    process = CrawlerProcess(overridden_settings)

    process.crawl(OnlinerApartmentSpider, url_file=args.url_file)
    process.start()


if __name__ == '__main__':
    main()
