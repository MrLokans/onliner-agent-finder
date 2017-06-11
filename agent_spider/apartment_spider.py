import re
import logging


import scrapy
from agent_spider.config import APARTMENT_OPTIONS
from agent_spider.finder import get_apartment_urls
from agent_spider.items import ApartmentBulletin
from agent_spider.loader import BulletinLoader
from agent_spider.url_cache import URLCacheManager


logger = logging.getLogger(__name__)


LONGITUDE_REGEX = re.compile(r'longitude = (?P<longitude>\d+\.\d+),')
LATITUDE_REGEX = re.compile(r'latitude = (?P<latitude>\d+\.\d+),')


def get_option_field(name: str) -> str:
    return 'has_{field}'.format(field=name)


class OnlinerApartmentSpider(scrapy.Spider):
    name = 'onliner_apartment_spider'

    def __init__(self,
                 url_file=None,
                 use_cache: bool=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._use_cache = use_cache
        if self._use_cache:
            logger.info('Spider cache is enabled. '
                        'Initialising cache manager.')
            self.cache_manager = URLCacheManager()
            self.cache_manager.load_cache()
        self.start_urls = self._get_start_urls(url_file)

    def closed(self, *args, **kwargs):
        if self._use_cache:
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

        if self._use_cache:
            urls = [url for url in urls
                    if not self.cache_manager.has_url(url)]
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
        loader.add_xpath('images',
                         '//div[contains(@class, "apartment-gallery__slide")]/@style')
        loader.add_xpath('description',
                         '//div[contains(@class, "apartment-info__sub-line_extended-bottom")]//text()')
        options_loader = loader.nested_xpath('//div[contains(@class, "apartment-options")]')
        for index_, (field_name, _) in enumerate(APARTMENT_OPTIONS):
            options_loader.add_xpath(get_option_field(field_name),
                                     self._get_option_xpath(index_))

        long, lat = self._extract_coordinates_from_script(response.text)
        loader.add_value('origin_url', response.url)
        loader.add_value('longitude', long)
        loader.add_value('latitude', lat)
        item = loader.load_item()
        if self._use_cache:
            self.cache_manager.add_url(response.url)
        yield item
