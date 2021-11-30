# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UkparlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    party = scrapy.Field()
    region = scrapy.Field()
    phonenumber = scrapy.Field()
    twitter = scrapy.Field()
    pass
