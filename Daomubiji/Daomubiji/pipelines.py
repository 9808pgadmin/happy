# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DaomubijiPipeline(object):
    def process_item(self, item, spider):

        filename = '..daomu/{}_{}_{}'.format(
            item['volume_name'],
            item['zh_num'],
            item['zh_name'],
        )
        with open(filename, 'w')as f:
            f.write(item['zh_content'])

        return item
