# -*- coding: utf-8 -*-

# 下载表情包的模块

def downloadgif(url,filename):
    import requests
    print("downloading")
    # 下面的url是其中一个表情包的地址，用于测试
    # url = 'http://emoji.qpic.cn/wx_emoji/I0h8WqrnM66bTjq0icU0QJ575IffednYXBt3PtlNJCS1E2evOeYvIhg/'
    r = requests.get(url)
    with open(filename, "wb") as code:
       code.write(r.content)