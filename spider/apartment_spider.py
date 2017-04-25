import os
import sys

import scrapy
from scrapy.loader import processors, ItemLoader

from spider.items import ApartmentBulletin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))
from config import URL_FILE


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
        self.start_urls = self._get_start_urls()

    def _get_start_urls(self):
        urls = []
        with open(URL_FILE) as f:
            urls = f.readlines()
            urls = [u.strip() for u in urls]
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
        yield item
