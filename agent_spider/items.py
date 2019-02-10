import scrapy


class BaseApartmentItem(scrapy.Item):

    bulletin_type = scrapy.Field()

    user_url = scrapy.Field()
    user_name = scrapy.Field()
    address = scrapy.Field()
    origin_url = scrapy.Field()
    price_USD = scrapy.Field()
    price_BYN = scrapy.Field()

    longitude = scrapy.Field()
    latitude = scrapy.Field()

    images = scrapy.Field()
    phones = scrapy.Field()

    description = scrapy.Field()

    created = scrapy.Field()
    last_updated = scrapy.Field()

    apartment_type = scrapy.Field()


class RentedApartmentBulletin(BaseApartmentItem):

    has_furniture = scrapy.Field()
    has_kitchen_furniture = scrapy.Field()
    has_oven = scrapy.Field()
    has_fridge = scrapy.Field()
    has_washing_machine = scrapy.Field()
    has_tv = scrapy.Field()
    has_internet = scrapy.Field()
    has_balcony = scrapy.Field()
    has_conditioner = scrapy.Field()


class SoldApartmentBulletin(BaseApartmentItem):

    floors = scrapy.Field()
    total_area = scrapy.Field()
    living_area = scrapy.Field()
    kitchen_area = scrapy.Field()

    house_type = scrapy.Field()
    balcony_details = scrapy.Field()
    parking_details = scrapy.Field()
    ceiling_details = scrapy.Field()
