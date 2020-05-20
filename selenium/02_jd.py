#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time
"""糗事百科"""
# browser = webdriver.PhantomJS()
# browser.get('https://www.qiushibaike.com/text/')
# xpath = '//div[@class="content"]/span'
# span = browser.find_element_by_xpath(xpath)
# print(span.text)

# browser = webdriver.Chrome()
# browser.get('https://search.jd.com/')
# xpath = '//div[@class="content"]/span'
# span = browser.find_element_by_xpath(xpath)
# print(span.text)

"""首页搜索框
//*[@id="key"]
首页搜索按钮
//*[@id="search"]/div/div[2]/button
商品页的 商品信息节点对象列表
//*[@id="J_goodsList"]/ul/li
"""


class JdSpider:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = 'https://www.jd.com/'
        self.i = 0
        pass

    def get_page(self):
        # 打开京东
        self.browser.get(self.url)
        # 搜索节点
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('python书')
        # 下一页节点
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        # 留出时间给页面加载
        time.sleep(2)

    def parse_page(self):
        # 把进度条拉到最下面 动态加载
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(2)
        # 匹配所有商品节点对象列表
        li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        for li in li_list:
            print(li.text)
            print('*'*50)
            self.i += 1
        pass

    def main(self):
        self.get_page()
        # while True:
        for i in range(2):
            self.parse_page()
            #  判断是否为最后一页
            if self.browser.page_source.find('pn-next disable') == -1:
                self.browser.find_element_by_class_name('pn-next').click()
                time.sleep(3)
            else:
                break
        print(self.i)
        pass


if __name__ == '__main__':
    spider = JdSpider()
    spider.main()
