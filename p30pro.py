#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 要注册个key才能实现微信消息推送。请访问Server酱（http://sc.ftqq.com）注册一个
# SCKEY:微信推送接口key
# wx_text:标题
# wx_desp:正文
SCKEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
wx_text = "华为P30pro存货监控"
wx_desp = ""

# record.json是否有变化
new_state = False
# 当前p30pro状态
p30s = []
# 上一次p30pro状态
p30s_history = []

# 此为招商银行掌上生活客户端的华为P30pro客户端的购买页面
url = 'https://ssl.mall.cmbchina.com/_CL5_/Product/GetGroupProducts'
body = {"productCommonSyno": "427505", "gbNo": ""}
headers = {'content-type': "application/x-www-form-urlencoded; charset=UTF-8", 'Content-Length': '30'}

# 获取页面状态json数据
response = requests.post(url, data=body, headers=headers)
# 返回信息
#print response.text
# 返回响应头
#print response.status_code
# 解析json
text = json.loads(response.text)



# 获取商品状态信息
# ParentValue:手机颜色
# Value:运存大小+内存大小
# IsSoldOut:是否卖光（True：缺货 / False：有货）
for x in text['Results']:
    p30 = {'ParentValue':x['ParentValue'], 'Value': x['Value'] ,'IsSoldOut': x['IsSoldOut']}
    p30s.append(p30)
# print p30s

# record.json为上次获取到的页面状态，判断文件是否存在
if not os.path.exists("./record.json"):
    print "不存在record.json，新建中..."
    with open("./record.json","w") as f:
        json.dump(p30s, f)
else:
    print "存在record.json，读取中..."
    with open("./record.json", 'r') as load_f:
        p30s_history = json.load(load_f)
        # print p30s_history
# print "p30s============="
# print p30s
# print "p30s_history============"
# print p30s_history

# 当前p30pro数据与上一次监控到的p30pro状态变化监控
for a in p30s:
    for b in p30s_history:
        if a['ParentValue'] == b[u'ParentValue'] and a['Value'] == b[u'Value']:
            if a['IsSoldOut'] == b[u'IsSoldOut']:
                print("%s %s %s" %(a['Value'],a['ParentValue'],a['IsSoldOut']))
            else:
                new_state = True
                if a['IsSoldOut'] == "True":
                    print("%s %s 卖光啦!" % (a['Value'], a['ParentValue'] ))
                else:
                    print("%s %s 有货啦!" % (a['Value'], a['ParentValue'] ))
                    wx_desp = a['ParentValue'] + "，" + a['Value'] + "，有货啦。"
                    # 调用Server酱微信通知接口
                    url = "https://sc.ftqq.com/" + SCKEY + ".send?text="+ wx_text +"&desp=" + wx_desp
                    requests.get(url)

if new_state:
    # p30pro有变化，更新到record.json
    print "状态有变化，更新record.json"
    with open("./record.json", "w") as f:
        json.dump(p30s, f)
