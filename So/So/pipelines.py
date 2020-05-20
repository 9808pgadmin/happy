# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 导入scrapy的图片管道类
import scrapy
from scrapy.pipelines.images import ImagesPipeline


# 1.继承ImagesPipeline
# 2.重写 类内方法
class SoPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['img_link'])
