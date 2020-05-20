#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import time

# 无界
options = webdriver.ChromeOptions()
options.add_argument('--headless')
# 创建浏览器对象
browser = webdriver.Chrome(options=options)
# 地址栏中输入百度URL
browser.get('http://www.baidu.com/')
# 向搜索框输入 赵丽颖
browser.find_element_by_id('kw').send_keys('赵丽颖')
# 点击百度一下
browser.find_element_by_id('su').click()

# 给出事件加载页面
time.sleep(2)
# print(browser.page_source.find('kw'))
browser.find_element_by_class_name('n').click()
# 关闭浏览器
# browser.quit()