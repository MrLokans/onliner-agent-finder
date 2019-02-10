import re
import logging


import scrapy
from agent_spider.config import APARTMENT_OPTIONS, SOLD_OPTIONS_INFO_FIELDS, SOLD_DETAIL_FIELDS, BulletinType, \
    RENTED_URL_PART, SOLD_URL_PART
from agent_spider.finder import get_apartment_urls
from agent_spider.items import RentedApartmentBulletin, SoldApartmentBulletin
from agent_spider.loader import SoldLoader, RentLoader
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
        self._init_cache()
        self.start_urls = self._get_start_urls(url_file)

    def closed(self, *args, **kwargs):
        if self._use_cache:
            self.cache_manager.dump_cache()

    def _init_cache(self):
        if self._use_cache:
            logger.info('Spider cache is enabled. '
                        'Initialising cache manager.')
            self.cache_manager = URLCacheManager()
            self.cache_manager.load_cache()

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
        loader = self._get_loader_for_response(response)
        loader = self._configure_common_loader(loader, response)
        item = loader.load_item()
        if self._use_cache:
            self.cache_manager.add_url(response.url)
        yield item

    def _configure_common_loader(self, loader, response):

        loader.add_xpath('phones',
                         '//ul[contains(@class, "apartment-info__list_phones")]//li//a//text()')
        loader.add_xpath('user_name',
                         '(//div[contains(@class, "apartment-info__sub-line_extended")]//a)[last() - 1]//text()')
        loader.add_xpath('user_url',
                         '(//div[contains(@class, "apartment-info__sub-line_extended")]//a)[last() - 1]/@href')
        loader.add_xpath('address',
                         '//div[contains(@class, "apartment-info__sub-line apartment-info__sub-line_large")]//text()')
        loader.add_xpath('price_BYN',
                         '//span[contains(@class, "apartment-bar__price-value_primary")]//text()')
        loader.add_xpath('price_USD',
                         '//span[contains(@class, "apartment-bar__price-value_complementary")]//text()')
        loader.add_xpath('apartment_type',
                         '//span[contains(@class, "apartment-bar__value")]//text()')
        loader.add_xpath('images',
                         '//div[contains(@class, "apartment-gallery__slide")]/@style')
        loader.add_xpath('description',
                         '//div[contains(@class, "apartment-info__sub-line_extended-bottom")]//text()')
        loader.add_xpath('last_updated',
                         '//div[contains(@id, "apartment-up__last-time")]//text()')
        long, lat = self._extract_coordinates_from_script(response.text)
        url = response.url
        loader.add_value('origin_url', url)
        loader.add_value('longitude', long)
        loader.add_value('latitude', lat)
        return loader

    def _configure_rented_loader(self, loader, response):
        options_loader = loader.nested_xpath('//div[contains(@class, "apartment-options")]')
        for index_, (field_name, _) in enumerate(APARTMENT_OPTIONS):
            options_loader.add_xpath(get_option_field(field_name),
                                     self._get_option_xpath(index_))
        loader.add_value("bulletin_type", BulletinType.RENTED)
        return loader

    def _configure_sold_loader(self, loader, response):
        options_texts = response.xpath('//td[contains(@class, "apartment-options-table__cell_right")]//text()')
        for option_index, field_name in SOLD_OPTIONS_INFO_FIELDS:
            selector_result = options_texts[option_index]
            loader.add_value(field_name, selector_result.extract())

        details_texts = response.xpath('//li[contains(@class, "apartment-options__item")]//text()')
        for field_name, details_element in zip(SOLD_DETAIL_FIELDS, details_texts):
            loader.add_value(field_name, details_element.extract())
        loader.add_value("bulletin_type", BulletinType.SOLD)
        return loader

    def _get_loader_for_response(self, response):
        url = response.url
        if SOLD_URL_PART in url:
            loader = SoldLoader(item=SoldApartmentBulletin(), response=response)
            return self._configure_sold_loader(loader, response)
        elif RENTED_URL_PART in url:
            loader = RentLoader(item=RentedApartmentBulletin(), response=response)
            return self._configure_rented_loader(loader, response)
        else:
            raise ValueError("Unknown url to parse: {}".format(url))
