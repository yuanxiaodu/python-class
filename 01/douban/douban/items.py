# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    votes = scrapy.Field()
    name = scrapy.Field()
    seen = scrapy.Field()
    star = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    # pass
