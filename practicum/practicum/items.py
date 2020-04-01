# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# required package for running this file completely
import scrapy


# This class statement will be called by all spiders that have from "..items import PracticumItem"
# specified at the top 0f the file.
class PracticumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_url = scrapy.Field()
    twitter = scrapy.Field()
    author = scrapy.Field()
    article_title = scrapy.Field()
    article_date = scrapy.Field()
    article_text = scrapy.Field()
    timestamp = scrapy.Field()
    pass
