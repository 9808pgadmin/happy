#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import execjs
import requests


class BaiduTranslateSpider:
    def __init__(self):
        self.get_url = 'https://fanyi.baidu.com/?aldtype=16047'
        self.headers = {'user-agent': 'Mozilla/5.0'}
        self.post_url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        pass

    def get_token(self):
        html = requests.get(url=self.get_url,
                            headers=self.headers).text
        pattern = re.compile("token: '(.*?)'", re.S)
        gtk = re.compile(".*?window.*?gtk = '(.*?)';</script>", re.S)
        # 列表
        token = pattern.findall(html)[0]
        window_gtk = gtk.findall(html)[0]
        return token, window_gtk

    def get_sign(self):
        with open('node.js', 'r') as f:
            js_data = f.read()
        # 创建对象
        exec_object = execjs.compile(js_data)
        sign = exec_object.eval('e("{}")'.format(word))
        return sign

    def get_result(self, word, fro, to):
        token, gtk = self.get_token()
        sign = self.get_sign()
        data = {
            'rom': fro,
            'to': to,
            'query': word,
            'transtype': 'realtime',
            'simple_means_flag': '3',
            'sign': sign,
            'token': token,
            'domain': 'common',
        }
        r = requests.post(self.post_url, data=data, heasers=self.headers)
        print(r.json()['trans_result']['data'][0]['dst'])
        # return result


if __name__ == '__main__':
    spider=BaiduTranslateSpider()
    menu = '1.英译汉 2.汉译英'
    choice = input('1.英译汉 2.汉译英')
    word = input('输入要翻译的单词')
    if choice == '1':
        fro = 'en'
        to = 'zh'
    elif choice == '2':
        fro = 'zh'
        to = 'en'
    spider.main(word, fro, to)

