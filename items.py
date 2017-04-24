import scrapy


class ApartmentBulletin(scrapy.Item):
    phones = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    origin_url = scrapy.Field()
