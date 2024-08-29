# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SnatcherItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    image = scrapy.Field()
    site = scrapy.Field()

