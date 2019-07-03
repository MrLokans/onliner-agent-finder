import html2text
from scrapy.loader import (
    processors,
    ItemLoader
)
from scrapy.selector import Selector

from agent_spider.config import (
    APARTMENT_OPTIONS,
    ONLINER_IMAGE_REGEX,
    OPTION_NOT_SELECTED_CLASS,
)


html_processor = html2text.HTML2Text()


def parse_options_block(block):
    sel = Selector(text=block)
    return not sel.css(".{}".format(OPTION_NOT_SELECTED_CLASS))


def parse_bulletin_images(text):
    """
    We need to extract image URLs from
    the style attribute.
    """
    # TODO: add missing URL handling
    match = ONLINER_IMAGE_REGEX.search(text)
    if match:
        return match.group()
    else:
        return ''


def parse_square_meters_value(value: str) -> float:
    if value == 'Кухня совмещена с жилой':
        return 0.0
    return float(value.replace('\xa0', ' ').replace('м', '').replace(',', '.').strip())


class BaseLoader(ItemLoader):

    default_output_processor = processors.TakeFirst()

    user_url_in = processors.MapCompose(lambda s: s)
    user_name_in = processors.MapCompose(lambda s: s.strip())
    phones_in = processors.MapCompose(lambda s: s.replace(' ', '')
                                                 .replace('-', ''))
    phones_out = processors.MapCompose("".join)
    address_in = processors.MapCompose(lambda s: s.strip())
    apartment_type_in = processors.MapCompose(lambda s: s.strip())

    owner_type = processors.MapCompose(lambda s: s.strip())

    price_BYN_in = processors.MapCompose(lambda s: s.replace('р.', '').replace(',', '.').strip())
    price_USD_in = processors.MapCompose(lambda s: s.replace('$', '').strip())

    images_in = processors.MapCompose(parse_bulletin_images)
    images_out = processors.MapCompose("".join)

    last_updated_in = processors.MapCompose(lambda s: s.strip())
    description_out = processors.MapCompose(html_processor.handle)


class RentLoader(BaseLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_apartment_options_fields_to_loader()

    def add_apartment_options_fields_to_loader(self):
        for field_name, _ in APARTMENT_OPTIONS:
            setattr(self,
                    "has_{}_in".format(field_name),
                    processors.MapCompose(parse_options_block))


class SoldLoader(BaseLoader):
    floors_in = processors.MapCompose(lambda s: s.strip())
    kitchen_area_in = processors.MapCompose(parse_square_meters_value)
    total_area_in = processors.MapCompose(parse_square_meters_value)
    living_area_in = processors.MapCompose(parse_square_meters_value)

    house_type = processors.MapCompose(lambda s: s)
    balcony_details = processors.MapCompose(lambda s: s)
    parking_details = processors.MapCompose(lambda s: s)
    ceiling_details = processors.MapCompose(lambda s: s)
