# -*- coding: utf-8 -*-
import json
from ..items import SoItem
import scrapy

"""图片爬取--非结构化数据"""


class SoSpider(scrapy.Spider):
    name = 'so'
    allowed_domains = ['image.so.com']
    # start_urls = ['http://image.so.com/']

    # 重写
    def start_requests(self):
        url = 'https://image.so.com/zjl?ch=beauty&sn={}&listtype=new&temp=1'
        for i in range(2):
            sn = i*30
            full_url = url.format(sn)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse
            )

    def parse(self, response):
        html = json.loads(response.text)
        item = SoItem()
        # 提取图片链接
        for img in html['list']:
            item['img_link'] = img['qhimg_url']

            yield item
        pass
