#!/usr/bin/env python

import argparse
import logging

from scrapy.crawler import CrawlerProcess

from agent_spider import settings
from agent_spider.apartment_spider import OnlinerApartmentSpider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging\
    .getLogger('urllib3.connectionpool')\
    .setLevel(logging.WARNING)
logging.getLogger('scrapy.*').setLevel(logging.INFO)


DEFAULT_OUTPUT_FILE = 'bulletins.json'


class SpiderLauncher:

    def __init__(self,
                 local_settings: dict = None,
                 url_cache=None,
                 url_file: str = None):
        self._settings = self._read_default_settings()
        if local_settings:
            self._settings.update(local_settings)
        self._url_cache = url_cache
        self._url_file = url_file

    @staticmethod
    def _read_default_settings():
        """
        Reads spider settings and returns
        dictionary of settings.
        """
        global settings
        return {s: getattr(settings, s)
                for s in dir(settings)
                if s.isupper()}

    def run(self):
        process = CrawlerProcess(self._settings)
        process.crawl(OnlinerApartmentSpider,
                      url_cache=self._url_cache,
                      url_file=self._url_file)
        process.start()


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
    overridden_settings = {
        'FEED_FORMAT': args.output_file.split('.')[-1],
        'FEED_URI': args.output_file,
        'SPIDER_LOADER_WARN_ONLY': True,
        'LOG_LEVEL': 'INFO',
    }
    launcher = SpiderLauncher(local_settings=overridden_settings,
                              url_file=args.url_file,
                              use_cache=args.use_cache)
    launcher.run()


if __name__ == '__main__':
    main()
