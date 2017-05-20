import scrapy


class ApartmentBulletin(scrapy.Item):
    phones = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    origin_url = scrapy.Field()
    price_USD = scrapy.Field()
    apartment_type = scrapy.Field()

    longitude = scrapy.Field()
    latitude = scrapy.Field()

    has_furniture = scrapy.Field()
    has_kitchen_furniture = scrapy.Field()
    has_oven = scrapy.Field()
    has_fridge = scrapy.Field()
    has_washing_machine = scrapy.Field()
    has_tv = scrapy.Field()
    has_internet = scrapy.Field()
    has_balcony = scrapy.Field()
    has_conditioner = scrapy.Field()
