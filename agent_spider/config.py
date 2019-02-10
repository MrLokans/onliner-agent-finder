import re

DEFAULT_URL_FILE = 'apartment_urls.txt'


SEARCH_RENT_BASE_URL = ''

RENTED_APARTMENTS_SEARCH_API_URL = 'https://ak.api.onliner.by/search/apartments'
SOLD_APARTMENTS_SEARCH_API_URL = 'https://pk.api.onliner.by/search/apartments'
LAT_INDEX, LONG_INDEX = 0, 1
RENT_TYPE = '2_rooms'

MINSK_BOUND_COORDINTATES = {
    # Left bottom corner
    'lb': ('53.78873227020693', '27.25622458457113'),
    # Right top corner
    'rt': ('54.01559842227507', '27.86870368988288')
}
CACHE_FILENAME = 'spider_url_cache.pickle'


APARTMENT_OPTIONS = (
    ("furniture", "Мебель"),
    ("kitchen_furniture", "Кухонная мебель"),
    ("oven", "Плита"),
    ("fridge", "Холодильник"),
    ("washing_machine", "Стиральная машина"),
    ("tv", "Телевизор"),
    ("internet", "Интернет"),
    ("balcony", "Лоджия или балкон"),
    ("conditioner", "Кондиционер"),
)

SOLD_OPTIONS_INFO_FIELDS = (
    # Index in xpath results list, item field name
    (0, 'floors'),
    (1, 'total_area'),
    (4, 'living_area'),
    (7, 'kitchen_area'),
)
SOLD_DETAIL_FIELDS = (
    'apartment_type',
    'house_type',
    'balcony_details',
    'parking_details',
    'ceiling_details',
)

OPTION_NOT_SELECTED_CLASS = 'apartment-options__item_lack'
ONLINER_IMAGE_REGEX = re.compile(r'(?:http|https):\/\/[a-zA-Z0-9_\/\.\-]+\.(?:jpeg|jpg|png|gif)')


class BulletinType:
    RENTED = 'RENTED'
    SOLD = 'SOLD'


RENTED_URL_PART = '/ak/'
SOLD_URL_PART = '/pk/'
