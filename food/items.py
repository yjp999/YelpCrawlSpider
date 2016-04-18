# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    category = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    location = scrapy.Field()
