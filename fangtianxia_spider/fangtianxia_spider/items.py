# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province=scrapy.Field()
    city=scrapy.Field()
    name=scrapy.Field()
    price=scrapy.Field()
    rooms=scrapy.Field()
    area=scrapy.Field()
    address=scrapy.Field()

    sale=scrapy.Field()
    origin_url=scrapy.Field()

class ESFItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    year = scrapy.Field()
    unity = scrapy.Field()
    origin_url = scrapy.Field()