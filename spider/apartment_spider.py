import os
import sys
import logging

import scrapy
from scrapy.loader import (
    processors,
    ItemLoader
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))

from spider.finder import get_apartment_urls
from spider.items import ApartmentBulletin
from spider.url_cache import URLCacheManager

logger = logging.getLogger(__name__)


class BulletinLoader(ItemLoader):
    default_input_processor = processors.Identity()
    default_output_processor = processors.TakeFirst()

    url_in = processors.MapCompose(lambda s: s)
    phones_in = processors.MapCompose(lambda s: s.replace(' ', '').replace('-', ''))
    phones_out = processors.MapCompose(lambda l: "".join(l))
    name_in = processors.MapCompose(lambda s: s.strip())
    address_in = processors.MapCompose(lambda s: s.strip())


class OnlinerApartmentSpider(scrapy.Spider):
    name = 'onliner_apartment_spider'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_manager = URLCacheManager()
        self.cache_manager.load_cache()
        self.start_urls = self._get_start_urls()

    def closed(self, *args, **kwargs):
        self.cache_manager.dump_cache()

    def _get_start_urls(self):
        use_file = os.environ.get('SPIDER_USE_URL_FILE')
        cache_file = os.environ.get('SPIDER_URL_FILE')
        if use_file and cache_file:
            logger.info("Using URL file %s", cache_file)
            with open(cache_file) as f:
                urls = f.readlines()
                urls = [u.strip() for u in urls]
        else:
            logger.info("Obtaining URL from onliner website")
            urls = list(get_apartment_urls())

        urls = [url for url in urls if not self.cache_manager.has_url(url)]
        return urls

    def parse(self, response):
        loader = BulletinLoader(ApartmentBulletin(), response)
        loader.add_xpath('phones',
                         '//ul[contains(@class, "apartment-info__list_phones")]//li//a//text()')
        loader.add_xpath('url',
                         '(//div[contains(@class, "apartment-info__sub-line_extended")]//a)[last()]/@href')
        loader.add_xpath('name',
                         '(//div[contains(@class, "apartment-info__sub-line_extended")]//a)[last()]/text()')
        loader.add_xpath('address',
                         '//div[contains(@class, "apartment-info__sub-line apartment-info__sub-line_large")]//text()')
        loader.add_value('origin_url', response.url)
        item = loader.load_item()
        self.cache_manager.add_url(response.url)
        yield item
