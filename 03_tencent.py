#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
import time

import requests


class TencentSpider():
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0'}
        self.one_url ="https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1589437103625&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn"
        self.two_url ="https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1589437285033&postId={}&language=zh-cn"

    # 请求函数
    def get_page(self, url):
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        return json.loads(res.text)

    # 获取数据
    def get_data(self, html):
        job_info = {}
        print(html['Data']['Posts'])
        for job in html['Data']['Posts']:
            job_info['job_name'] = job['RecruitPostName']
            post_id = job['PostId']
            two_url = self.two_url.format(post_id)
            job_info['job_duty'], job_info['require'] = self.parse_two_page(two_url)
            # print(job_info)

    def parse_two_page(self, two_url):
        two_html = self.get_page(two_url)
        duty = two_html['Data']['Responsibility']
        require = two_html['Data']['Requirement']
        return duty, require

    def main(self):
        for index in range(1, 11):
            url = self.one_url.format(index)
            one_html = self.get_page(url)
            self.get_page(one_html)
            time.sleep(random.uniform(1, 2))


if __name__ == '__main__':
    spider = TencentSpider()
    spider.main()