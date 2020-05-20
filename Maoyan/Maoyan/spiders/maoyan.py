# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4?offset=0']
    offset = 0

    def parse(self, response):
        # 基准xpath
        dd_lidt = response.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in dd_lidt:
            # 创建对象(类:items.py中的class MaoyanItem())
            item = MaoyanItem()
            item['name'] = dd.xpath('./a/@title').extract_first().strip()
            item['star'] = dd.xpath('.//p[@class="star"]/text()').extract_first().strip()
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').extract_first().strip()

            # 把爬取的数据交给管道文件pipline处理
            yield item
        # 用于拼接新的url交给调度器队列
        # self.offset += 10
        # if self.offset <= 90:
        #     url = 'https://maoyan.com/board/4?offset={}'.format(self.offset)
        #     # 交给调度器入队列
        #     yield scrapy.Request(
        #         url=url,
        #         callback=self.parse
        #     )