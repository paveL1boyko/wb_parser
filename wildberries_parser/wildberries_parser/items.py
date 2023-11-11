# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WildberriesSellerItem(scrapy.Item):
    name = scrapy.Field()
    seller_link = scrapy.Field()
    seller_logo_link = scrapy.Field()
    ogrn = scrapy.Field()
