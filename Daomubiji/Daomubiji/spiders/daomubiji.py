# -*- coding: utf-8 -*-
from ..items import DaomubijiItem
import scrapy
"""三级页面"""


class DaomubijiSpider(scrapy.Spider):
    name = 'daomubiji'
    allowed_domains = ['daomubiji.com']
    start_urls = ['http://daomubiji.com/']

    # 解析一级页面的parse函数
    def parse(self, response):
        link_list = response.xpath('//ul[@class="sub-menu"]/li/a/@href').extract()
        for link in link_list:
            yield scrapy.Request(
                url=link,
                callback=self.parse_two_html
            )

    # 解析二级页面函数(卷名  章节数 章节名 链接)
    def parse_two_html(self, response):
        # 基准xpath
        article_list = response.xpath('//article')
        for article in article_list:
            # 创建item对象
            item = DaomubijiItem()
            # info_list:  ['七星鲁王','第一章','血尸']
            info_list = article.xpath('./a/text()').get().split()
            if len(info_list) == 3:
                item['volume_name'] = info_list[0]
                item['zh_num'] = info_list[1]
                item['zh_name'] = info_list[2]
            else:
                item['volume_name'] = info_list[0]
                item['zh_name'] = info_list[1]
                item['zh_num'] = ''
            # 提取链接并发给调度器入队列
            item['zh_link'] = article.xpath('./a/@href').get()
            yield scrapy.Request(
                url=item['zh_link'],
                # meta参数  传递item对象到下一个解析函数
                meta={'item': item},
                callback=self.parse_three_html
            )

    # 解析三级页面(小说内容)函数
    def parse_three_html(self, response):
        # 获取上一个函数传递过来的item对象
        item = response.meta['item']
        # content_list: ['段落1','段落2','段落3',.....]
        content_list = response.xpath('//article[@class="article-content"]//p/text()').extract()
        item['zh_content'] = '\n'.join(content_list)
        yield item
