# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class Product(scrapy.Item):
    pid = scrapy.Field()
    item_num = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    review_count = scrapy.Field()
    review_score = scrapy.Field()
    brand = scrapy.Field()
    description_short = scrapy.Field()
    description_long = scrapy.Field()
    price = scrapy.Field()
    price_low = scrapy.Field()
    price_high = scrapy.Field()
    price_sale = scrapy.Field()
    image = scrapy.Field()
    condition = scrapy.Field()
    category = scrapy.Field()
    breadcrumbs = scrapy.Field()
    initial_data = scrapy.Field()
