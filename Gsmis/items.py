# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class GsmisItem(scrapy.Item):
    # define the fields for your item here like:
    name = Field()
    sex = Field()

    administrative = Field() # duties
    professional = Field()

    phone = Field()
    type = Field()

    education = Field()
    degree = Field()
    graduate = Field() # college

    email = Field()
    workunit = Field()

    resume = Field()

    academic = Field()
    achievement = Field()
    project = Field()

    postgraduate = Field()

    remark = Field()

    direction = Field()

class DirectionItem(scrapy.Item):

    subject = Field()
    code = Field()
    introduce = Field()