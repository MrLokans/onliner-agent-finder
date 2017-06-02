import os
import re
import sys
import logging

import scrapy
from scrapy.loader import (
    processors,
    ItemLoader
)
from scrapy.selector import Selector

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))

from spider.config import (
    APARTMENT_OPTIONS,
    OPTION_NOT_SELECTED_CLASS
)
from spider.finder import get_apartment_urls
from spider.items import ApartmentBulletin
from spider.url_cache import URLCacheManager

logger = logging.getLogger(__name__)


LONGITUDE_REGEX = re.compile(r'longitude = (?P<longitude>\d+\.\d+),')
LATITUDE_REGEX = re.compile(r'latitude = (?P<latitude>\d+\.\d+),')


def get_option_field(name: str) -> str:
    return 'has_{field}'.format(field=name)


def parse_options_block(block):
    sel = Selector(text=block)
    return not sel.css(".{}".format(OPTION_NOT_SELECTED_CLASS))


class BulletinLoader(ItemLoader):
    default_input_processor = processors.Identity()
    default_output_processor = processors.TakeFirst()

    url_in = processors.MapCompose(lambda s: s)
    phones_in = processors.MapCompose(lambda s: s.replace(' ', '').replace('-', ''))
    phones_out = processors.MapCompose(lambda l: "".join(l))
    name_in = processors.MapCompose(lambda s: s.strip())
    address_in = processors.MapCompose(lambda s: s.strip())
    apartment_type_in = processors.MapCompose(lambda s: s.strip())
    price_USD_in = processors.MapCompose(lambda s: s.replace('$', '').strip())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_apartment_options_fields_to_loader()

    def add_apartment_options_fields_to_loader(self):
        for field_name, _ in APARTMENT_OPTIONS:
            setattr(self,
                    "has_{}_in".format(field_name),
                    processors.MapCompose(parse_options_block))


class OnlinerApartmentSpider(scrapy.Spider):
    name = 'onliner_apartment_spider'

    def __init__(self, url_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_manager = URLCacheManager()
        self.cache_manager.load_cache()
        self.start_urls = self._get_start_urls(url_file)

    def closed(self, *args, **kwargs):
        self.cache_manager.dump_cache()

    def _get_start_urls(self, url_file=None):
        if url_file:
            logger.info("Using URL file %s", url_file)
            with open(url_file) as f:
                urls = f.readlines()
                urls = [u.strip() for u in urls]
        else:
            logger.info("Obtaining URL from onliner website")
            urls = list(get_apartment_urls())

        urls = [url for url in urls if not self.cache_manager.has_url(url)]
        return urls

    def _get_option_xpath(self, option_index: int) -> str:
        return ('div[contains(@class, "apartment-options__item")][{idx}]'
                .format(idx=option_index + 1))

    def _extract_coordinates_from_script(self, text):
        # TODO: Attempt to avoid parsing the whole page twice
        # may be select specific <script> tag
        longitude = LONGITUDE_REGEX.search(text).groupdict()['longitude']
        latitude = LATITUDE_REGEX.search(text).groupdict()['latitude']
        return longitude, latitude

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
        loader.add_xpath('price_USD',
                         '//span[contains(@class, "apartment-bar__price-value_complementary")]//text()')
        loader.add_xpath('apartment_type',
                         '//span[contains(@class, "apartment-bar__value")]//text()')
        options_loader = loader.nested_xpath('//div[contains(@class, "apartment-options")]')
        for index_, (field_name, _) in enumerate(APARTMENT_OPTIONS):
            options_loader.add_xpath(get_option_field(field_name),
                                     self._get_option_xpath(index_))

        long, lat = self._extract_coordinates_from_script(response.text)
        loader.add_value('origin_url', response.url)
        loader.add_value('longitude', long)
        loader.add_value('latitude', lat)
        item = loader.load_item()
        self.cache_manager.add_url(response.url)
        yield item
