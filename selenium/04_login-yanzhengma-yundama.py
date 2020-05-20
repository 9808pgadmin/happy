#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
# 处理图片库
from PIL import Image

browser = webdriver.Chrome()


# 获取首页截图，为了抠出验证码图片
def get_screen_shot():
    browser.get('http://www.yundama.com/')
    # 获取首页截图
    browser.save_screenshot('index.png')


# 从首页截图中获取验证码图片
def get_caphe():
    # 定位验证码元素位置(x,y坐标)
    location = browser.find_element_by_xpath('//*[@id="verifyImg"]').location
    # 大小(宽度和高度)
    size = browser.find_element_by_xpath('//*[@id="verifyImg"]').size
    # 左上角x坐标
    left = location['x']
    # 左上角y坐标
    top = location['y']
    # 右下角x坐标
    right = left+size['width']
    # 右下角y坐标
    bottom = top + size['height']

    # 截取验证码图片   crop():对图片剪切，参数为元组
    img = Image.open('index.png').crop((left, top, right, bottom))
    img.save('verify.png')

    # 调用在线打码平台进行打码
    result = get_result('verify.png')
    return result


if __name__ == '__main__':
    get_screen_shot()
    result = get_caphe()
    print(result)

import http.client, mimetypes, urllib, json, time, requests


class YDMHttp:
    apiurl = 'http://api.yundama.com/api.php'
    username = ''
    password = ''
    appid = ''
    appkey = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response

    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid), 'flag': '0'}
        response = self.request(data)
        if (response):
            return response['ret']
        else:
            return -9001

    def post_url(self, url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb');
        res = requests.post(url, files=files, data=fields)
        return res.text


def get_result(filename):
    # 用户名
    username    = 'yibeizi001'
    # 密码
    password    = 'zhanshen002'
    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appid       = 1
    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appkey      = '22cc5376925e9387a23cf797cb9ba745'
    # 图片文件
    # filename    = 'getimage.jpg'
    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype    = 5000
    # 超时时间，秒
    timeout     = 60
    # 初始化
    yundama = YDMHttp(username, password, appid, appkey)
    # 登陆云打码
    uid = yundama.login();
    # 查询余额
    balance = yundama.balance();
    # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
    cid, result = yundama.decode(filename, codetype, timeout);
    return result