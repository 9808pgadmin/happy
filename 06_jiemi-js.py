#!/usr/bin/env python
# -*- coding: utf-8 -*-

import execjs
"""百度翻译---js中的参数sign:的获取"""
with open('node.js', 'r') as f:
    js_data = f.read()
# 创建对象
exec_object = execjs.compile(js_data)
sign = exec_object.eval('e("lion")')
print(sign)
"""# 在js中
	token: window.common.token
	# 在响应中想办法获取此值
	token_url = 'https://fanyi.baidu.com/?aldtype=16047'
	regex: "token: '(.*?)'"
	"""