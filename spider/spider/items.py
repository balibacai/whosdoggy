# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class RosterItem(scrapy.Item):
    detail = scrapy.Field()
    name = scrapy.Field()
    alias = scrapy.Field()


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    dog_name = scrapy.Field()
    image_base = scrapy.Field()
