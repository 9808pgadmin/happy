# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    # 爬虫名 :scrapy crawl 爬虫名
    name = 'baidu'
    # 允许爬取的域名
    allowed_domains = ['www.baidu.com']
    # 起始的url地址
    start_urls = ['http://www.baidu.com/']

    # response为http://www.baidu.com/的响应队象
    def parse(self, response):
        title = response.xpath('/html/head/title/text()').get()
        print('*'*40)
        print(title)
        print('*'*40)

