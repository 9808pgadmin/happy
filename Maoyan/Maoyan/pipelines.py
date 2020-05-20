# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from .settings import *


class MaoyanPipeline(object):
    # 处理数据
    def process_item(self, item, spider):
        print(item['name'])
        print(item['star'])
        print(item['time'])

        return item


# 定义一个Mysql管道类
class MaoyanMysqlPipline:
    # 爬虫开始执行1次,用于数据库连接
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
        print('我是open_spider函数')

    # 用于处理抓取的item数据
    def process_item(self, item, spider):
        ins = 'insert into tab values(%s,%s,%s)'
        film_list = [
            item['name'], item['star'], item['time']
        ]
        self.cursor.execute(ins, film_list)
        self.db.commit()

        # 必须写，此函数返回值会交给下一个管道继续处理item数据
        return item

    # 爬虫结束时执行1次,用于断开数据库连接
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
        print('我是colse_spider函数')


# import pymongo
# # 定义一个Mongo管道类
# class MaoyanMongoPipline:
#     # 爬虫开始执行1次,用于数据库连接
#     def open_spider(self, spider):
#         self.conn = pymongo.MongoClient(
#             host=MONGO_HOST,
#             port=MONGO_PORT,
#         )
#         # 库对象
#         self.db = self.conn['filmtab']
#         # 集合(表)对象
#         self.myset = self.db['tab']
#         print('我是open_spider函数')
#
#     # 用于处理抓取的item数据
#     def process_item(self, item, spider):
#         film_dict = {
#             '电影名称': item['name'],
#             '电影主演': item['star'],
#             '上映时间': item['time'],
#         }
#         # mongo数据库要放字典数据
#         self.myset.insert_one(film_dict)
#
#         # 必须写，此函数返回值会交给下一个管道继续处理item数据
#         return item
#     # mongo数据库不用关闭
#     # 查询数据  show dbs   use filmtab   db.tab.find