# -*- coding: utf-8 -*-

import scrapy
import functools
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from Gsmis.items import *

class GemisSpider(CrawlSpider):
    name = "gsmis"
    allowed_domains = ["gsmis.nuaa.edu.cn"]
    start_urls = (
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=001',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=002',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=003',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=004',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=005',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=006',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=007',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=008',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=009',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=010',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=011',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=012',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=015',
        'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/xkds.aspx?xsbh=017',
        # 'http://gsmis.nuaa.edu.cn:81/nuaagmis/xkjsb/yjsdsfc.aspx?id=04060'
    )

    rules = [
        Rule(LinkExtractor(allow='yjsdsfc.aspx\?id=\d+'), callback = 'parse_item')
    ]

    trans = {
        'name': 'lbldsxm',
        'sex' : 'lbldsxb',

        'administrative' : 'lblxzzw',
        'professional' : 'lblzc',

        'phone' : 'lbldwdh',
        'type' : 'lbldslb',

        'education' : 'lblxl',
        'degree' : 'lblxw',
        'graduate' : 'lblhxlyx',

        'email' : 'lblemail',
        'workunit' : 'lblgzdw',

        'resume' : 'txtgrjl',

        'academic' : 'lblxsrz',
        'achievement' : 'lblxscj',
        'project' : 'lbljf',

        'postgraduate' : 'lblbz',

        'remark' : 'txtbz'
    }

    def parse_item(self, response):
        getById = functools.partial(self.getById, response)

        item = GsmisItem()

        for key in self.trans:
            value = self.trans[key]
            item[key] = getById(value)

        item['direction'] = []

        subject = response.xpath('//span[re:test(@id, "lblcszym\d*$")]/text()').extract()
        code = response.xpath('//span[re:test(@id, "cszym\d*$")]/text()').extract()
        introduce = response.xpath('//span[re:test(@id, "lblyjfx\d*$")]/text()').extract()

        for i in range(len(subject)):
            dirItem = DirectionItem()

            dirItem['subject'] = subject[i] if len(subject) > i else None
            dirItem['code'] = code[i] if len(code) > i else None
            dirItem['introduce'] = introduce[i] if len(introduce) > i else None

            item['direction'].append(dirItem)

        yield item

        # filename = response.url.split('=')[-1]
        # filename = 'output/'+ filename[:2] + '/' + filename + '.html'
        #
        # with open(filename, 'w') as f:
        #     f.write(response.body)

    def getById(self, response, id, pos = 0, dom = 'span'):
        result = response.xpath('//%s[@id="%s"]/text()' % (dom, id)).extract()
        return result[pos] if len(result) > pos else None