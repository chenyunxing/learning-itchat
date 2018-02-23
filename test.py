# -*- coding: utf-8 -*-
import itchat
import xml.dom.minidom
# 导入自定义的下载表情包模块
import download
# 注册器，将下面一个函数注册用于接收文本类型消息
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    # print(msg['Text'])
    # print(msg)
    # 这个只是获取我的好友列表内的一个人，似乎每一次登录好友列表的UserName都会改变，需要这样重新获取
    # 我的方法是模糊搜索，昵称，备注等里有等于Mo的都会被搜索到，返回结果是一个列表
    a = itchat.search_friends(name='Mo')
    # 不带参数搜索的结果是自己
    b = itchat.search_friends()
    # 进行回复，如果是我的a好友则每次他发来什么消息，我就回复什么消息
    if msg['FromUserName'] == a[0]['UserName']:
        # print内的函数是itchat的发送函数，第一个参数是发送文本内容，第二个是接受人的UserName
        print(itchat.send(msg['Text'], toUserName=a[0]['UserName']))
    elif msg['FromUserName'] == b['UserName']:
        print(itchat.send('我就是你，你发什么消息，傻啊', toUserName=b['UserName']))
# 注册器，用于监听发送的图片类型信息
@itchat.msg_register(itchat.content.PICTURE)
def test_content(msg):
    print(msg['MsgType'])
    print(msg)
    a = itchat.search_friends(name='Mo')
    b = itchat.search_friends()
    if (msg['FromUserName'] == a[0]['UserName']) & (msg['MsgType'] == 47):
        print(itchat.send(msg['Text'], toUserName=a[0]['UserName']))
        # 如果是自定义表情包，即可用下载的表情包则下载后发送
        if msg['HasProductId'] == 0:
            # 自定义的下载函数
            download.downloadgif(geturl(msg['Content']), "a.gif")
            # 这个发送函数也可以发送其他类型的文件，格式可以看 https://itchat.readthedocs.io/zh/latest/intro/reply/
            print(itchat.send('@img@%s' % 'a.gif', toUserName='filehelper'))
        # 否则是商店表情包则无法下载发送
        else:
            print(itchat.send('大佬，你赢了，这个表情我发不了', toUserName='filehelper'))
    elif (msg['ToUserName'] == 'filehelper') & (msg['MsgType'] == 47):
        # 如果是自定义表情包，即可用下载的表情包则下载后发送
        if msg['HasProductId'] == 0:
            download.downloadgif(geturl(msg['Content']),"a.gif")
            print(itchat.send('@img@%s' % 'a.gif', toUserName='filehelper'))
        else :
            print(itchat.send('大佬，你赢了，这个表情我发不了', toUserName='filehelper'))
# 自己写的一个获取xml内表情包url地址的函数
def geturl(gifxml):
    #将字符串解析成dom格式
    dom = xml.dom.minidom.parseString(gifxml)
    # 得到文档元素对象
    root = dom.documentElement
    # 获取节点
    urlxml = root.getElementsByTagName('emoji')[0]
    # print(urlxml.getAttribute("cdnurl"))
    # 返回节点中的属性
    return urlxml.getAttribute("cdnurl")
# 写的两个登录成功和退出成功的回调函数
def lc():
    print('登录成功')
def ec():
    print('已退出')
# 设置登录相关函数，hotReload是是否保存登录状态，选择True后可以不用每一次都进行扫码登录
# loginCallback是设置登录成功的回调函数
# exitCallback是设置退出成功的回调函数
itchat.auto_login(hotReload=True,loginCallback=lc, exitCallback=ec)
# 个人理解是加进线程持久运行，并未参考文档，加这个函数后可以跑起各个注册器
itchat.run()


# 下面是官网的一段代码，自己添加了一点注释，不过要注意一点，注册器写法已经改变，下面的代码不适用与python3
# 并未实践下列官网代码，下列代码应该是针对python2的，查看时自我斟酌修改
# 要一次注册多个应该这样
# @itchat.msg_register([itchat.content.TEXT, itchat.content.MAP, itchat.content.CARD, itchat.content.NOTE, itchat.content.SHARING])

# import itchat, time
# from itchat.content import *
# 注册文本，地图，名片，系统消息，分享消息
# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
# def text_reply(msg):
#     msg.user.send('%s: %s' % (msg.type, msg.text))
# 注册图片，语音，附件，小视频[注意，表情包也归属图片]
# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def download_files(msg):
#     msg.download(msg.fileName)
#     typeSymbol = {
#         PICTURE: 'img',
#         VIDEO: 'vid', }.get(msg.type, 'fil')
#     return '@%s@%s' % (typeSymbol, msg.fileName)
# 注册好友请求
# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     msg.user.verify()
#     msg.user.send('Nice to meet you!')
# 注册群消息
# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     if msg.isAt:
#         msg.user.send(u'@%s\u2005I received: %s' % (
#             msg.actualNickName, msg.text))
#
# itchat.auto_login(True)
# itchat.run(True)
