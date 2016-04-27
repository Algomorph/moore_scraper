# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Grant(scrapy.Item):
    name = scrapy.Field()
    organization = scrapy.Field()
    date_awarded = scrapy.Field(serializer=str)
    amount = scrapy.Field(serializer=str)
    term = scrapy.Field(serializer=str)
    id = scrapy.Field(serializer=str)
    funding_area = scrapy.Field(serializer=str)
    url = scrapy.Field(serializer=str)
