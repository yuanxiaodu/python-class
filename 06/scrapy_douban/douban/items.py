# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


class MovieCommentItem(Item):
    # define the fields for your item here like:
    name = Field()
    seen = Field()
    star = Field()
    date = Field()
    votes = Field()
    text = Field()
