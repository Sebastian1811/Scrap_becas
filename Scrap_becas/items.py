# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Becas(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    requirements = scrapy.Field()
    study_level =scrapy.Field()
    study_field = scrapy.Field()
    country_host = scrapy.Field()