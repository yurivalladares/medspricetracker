# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MedpricesItem(scrapy.Item):

    product_name = scrapy.Field()
    manufacturer = scrapy.Field()
    price = scrapy.Field()
    product_url = scrapy.Field()
    scraped_at = scrapy.Field(serializer=str)
    store = scrapy.Field()

    pass
