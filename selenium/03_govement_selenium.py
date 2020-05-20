#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import pymysql


class GovementSpider:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.one_url = 'http://www.mca.gov.cn/article/sj/xzqh/2020/'
        # 数据库相关变量
        self.db = pymysql.connect('localhost', 'root', '123456', 'govdb', charset='utf8')
        self.cursor = self.db.cursor()
        # 定义三个列表，为了excutemany()
        self.province_list = []
        self.city_list = []
        self.county_list = []
        pass

    # 获取首页,并提取二级页面链接（虚拟链接）
    def get_false_url(self):
        self.browser.get(self.one_url)
        # 提取二级页面链接 + 点击
        td_list = self.browser.find_elements_by_xpath(
            '//td[@class="arlisttd"]/a[contains(@title,"代码")]')
        if td_list:
            # 找到节点对象，以为要click()
            two_url_element = td_list[0]
            # 增量爬取,取出连接和数据库version表中做对比
            two_url = two_url_element.get_attribute('href')
            sel = 'select * from version where link="%s"'
            self.cursor.execute(sel, [two_url])
            result = self.cursor.fetchall()
            if result:
                print("数据已最新，无需爬取")
            else:
                two_url_element.click()
                time.sleep(2)
                # 切换browser
                all_handles = self.browser.window_handles
                self.browser.switch_to_window(all_handles[1])
                # 数据抓取
                self.get_data()
                # 结束之后把two_url插入到version表中
                ins = 'inser into version values(%s)'
                self.cursor.execute(ins, [two_url])
                self.db.commit()

    # 二级页面中提取行政区划代码
    def get_data(self):
        tr_list = self.browser.find_elements_by_xpath(
            '//tr[@height="10"]'
        )
        for tr in tr_list:
            code = tr.find_element_by_xpath('./td[2]').text.strip()
            name = tr.find_element_by_xpath('./td[3]').text.strip()
            # 判断层级关系,添加到对应的数据库表中
            if code[-4:] == "0000":
                self.province_list.append([name, code])
                # 单独判断4个直辖市放到city表中
                if name in ['北京市', '天津市', '上海市', '成都市']:
                    city = [name, code, code[:2] + "0000"]
                    self.city_list.append(city)
            elif code[-2:] == "00":
                city = [name, code, code[:2]+"0000"]
                self.city_list.append(city)
            else:
                if code[:2] in ['11', '12', '31', '50']:
                    county = [name, code, code[:2] + "0000"]
                else:
                    county = [name, code, code[:4] + "00"]
                self.county_list.append(county)
        self.insert_mysql()

    def insert_mysql(self):
        # 更新时一定要先删除表记录
        del_province = 'delete from province'
        del_city = 'delete from city'
        del_county = 'delete from county'
        self.cursor.execute(del_province)
        self.cursor.execute(del_city)
        self.cursor.execute(del_county)
        # 插入新的数据
        ins_province = "insert into province values(%s,%s)"
        ins_city = "insert into city values(%s,%s,%s)"
        ins_county = "insert into county values(%s,%s,%s)"
        self.cursor.executemany(ins_province, self.province_list)
        self.cursor.executemany(ins_city, self.city_list)
        self.cursor.executemany(ins_county, self.county_list)
        self.db.commit()
        print("数据抓取完成")

    def main(self):
        self.get_false_url()
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    spider = GovementSpider()
    spider.main()
