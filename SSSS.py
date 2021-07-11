#!/usr/bin/env python3
#
# from telethon import TelegramClient
#
# api_id = 6954260 #申请的TG API ID
# api_hash = 'b04a9cf820f26cc2b2b50ed9fb33bc75' #申请的TG API hash
#
# with TelegramClient('anon', api_id, api_hash) as client: #anon为缓存的授权密钥，可为其指定位置，比如想让anon存在于/etc下，这里的就换成/etc/anon
#     client.loop.run_until_complete(client.send_message('@DdD_dak', 'Hello, myself!')) #代码中的me为收信人的用户名，Hello, myself!为发送内容。比如想给用户名为@vay，发送一句hello world。这里就替换成('@vay', 'hello world')
import json
import requests
import os

def GetCfid(url,headers):
    d=[]
    u=[]
    g=dict()
    f = open("D:\\D文档\\新建文件夹\\test\\22\\domain.txt", 'r')
    result = list()
    for x in open("D:\\D文档\\新建文件夹\\test\\22\\domain.txt", 'r'):
        x = f.readline()
        result.append(x)
        if len(result) > 0:
            urls = url + "?name=" + x
            ret = requests.get(urls, headers=headers)
            res = ret.json()['result']
            for i in res:
                # print(i['id'])
                d.append(i['id'])
            if len(d) > 0:
                for idx, val in enumerate(d):
                    urls = url + "/" + val + "/dns_records"
                    rer = requests.get(urls, headers=headers)
                    rers = rer.json()['result']
                    if len(rers) > 0:
                        h = []
                        for l in rers:
                            # print(l['id'])
                            h.append(l['id'])
                            u.append(l['id'])
                        g[val] = h
                    else:
                        print("域名下没有解析记录,继续下一步")
                        h = []
                        for l in rers:
                            h.append(l['id'])
                            u.append(l['id'])
                        g[val] = h
            else:
                print("此账号下没有解析,继续下一步")
        else:
            print("请添加域名再执行")
    return g  #返回的是字典,{域名的区域id:[域名的每个解析id]}
#def Urlpinjie(url,headers,listu1=[],listu2=[]):

def CreateCf(url,headersn,host,org_name,org_id,lists=[],sslist=[]):
    url=url
    headers=headersn
    host=host
    lists=lists
    org_name=org_name
    org_id=org_id
    sslist=sslist
    print("添加之前会删除之前的域名 和 域名解析")
    # 添加域名之前先执行删除命令,不管他前面是否存在
    DelelteCf(url, headers, listwq=[],listwl=[])
    f = open("D:\\D文档\\新建文件夹\\test\\22\\domain.txt", 'r')
    result = list()
    for x in open("D:\\D文档\\新建文件夹\\test\\22\\domain.txt", 'r'):
        x = f.readline()
        result.append(x)
        if len(result) > 0:
            requestDataa = {"name": x,
                            "jump_start": True,
                            "organization": {"name": org_name,
                                             "id": org_id}}
            retd = requests.delete(url, json=requestDataa, headers=headers)
            # 然后执行post 添加域名
            print("先添加域名")
            reta = requests.post(url, json=requestDataa, headers=headers)
        else:
            print("请添加域名再执行")
    # 然后拿到域名的区域id
    dictc1 = GetCfid(url, headers)
    # 然后遍历数组,添加@,m,www解析
    for value, name in dictc1.items():
        if len(name) > 0:
            DelelteCf(url, headers, listwq=[], listwl=[])
        else:
            for ids, vals in enumerate(lists):
                requestData = {"type": "A",
                               "name": vals,
                               "content": host,
                               "ttl": 300,
                               "priority": 10,
                               "proxied": False}
                urls = url + "/" + value + "/dns_records"
                ret1 = requests.post(urls, json=requestData, headers=headers)
                ym = ret1.json()['result']['name']
                lx = ret1.json()['result']['type']
                mc = ret1.json()['result']['zone_id']
                ip = host
                jg = ret1.json()['success']
                if ret1.json()['success']:
                    print("域名:%-19s 记录类型:%-4s 解析名称:%-9s 解析ip:%-14s 结果:%s" % (ym, lx, mc, ip, jg))
                else:
                    print("域名:%-19s 记录类型:%-4s 解析名称:%-9s 解析ip:%-14s 结果:%s" % (ym, lx, mc, ip, jg))
            if len(sslist) > 0:
                requestDatassl = {"type": "CNAME",
                                  "name": sslist[0],
                                  "content": sslist[1],
                                  "ttl": 300,
                                  "priority": 10,
                                  "proxied": False}
                ret2 = requests.post(urls, json=requestDatassl, headers=headers)
                print(ret2)
                ym = ret2.json()['result']['name']
                lx = ret2.json()['result']['type']
                mc = ret1.json()['result']['zone_id']
                ip = host
                jg = ret2.json()['success']
                if ret2.json()['success']:
                    print("域名:%-19s 记录类型:%-4s 解析名称:%-12s 解析ip:%-14s 结果:%s" % (ym, lx, mc, ip, jg))
                else:
                    print("域名:%-19s 记录类型:%-4s 解析名称:%-12s 解析ip:%-14s 结果:%s" % (ym, lx, mc, ip, jg))
            else:
                print("此域名不在CF添加证书解析")


def DelelteCf(url,headersn,listwq=[],listwl=[]):
    url=url
    headers=headersn
    dictd1=GetCfid(url,headers)
    for value, name in dictd1.items():
        if len(name) > 0:
            for i, val in enumerate(name):
                urls = url +"/"+ value + "/dns_records"+"/" + val
                print(urls)
                ret = requests.delete(urls, headers=headers)
                if ret.json()['success']:
                    print("%s 删除成功" % val)
                else:
                    print("%s 删除失败" % val)
        else:
            print("检测没有这个解析,继续下一步")

def PathSsl(url,headers,listssl=[]):
    dictd1 = GetCfid(url, headers)
    listssl=listssl
    listtls=["off", "flexible", "full", "strict"]
    listset=["on","off"]
    if listssl[0] in listtls and listssl[1] in listset:
        for value, name in dictd1.items():
            urlssl = url + "/" + value  + "/settings/ssl"
            urlal = url + "/" + value  + "/settings/always_use_https"
            requestDatassl={"value":listssl[0]}
            requestDataal = {"id":"always_use_https","value":listssl[1]}
            ret = requests.patch(urlssl, json=requestDatassl, headers=headers)
            rel = requests.patch(urlal, json=requestDataal, headers=headers)
    else:
        print("listssl列表参数有误,请修改")


def Clean_purge_everything():
    # 然后拿到域名的区域id
    dictc1 = GetCfid(url, headers)
    for value, name in dictc1.items():
        print(value)
        requestData={"purge_everything":True}
        urls1=url +"/" +value
        urls2=url +"/" +value+"/purge_cache"
        ret1 = requests.get(urls1, json=requestData, headers=headers)
        ret2 = requests.post(urls2, json=requestData, headers=headers)
        ym = ret1.json()['result']['name']
        jg = ret2.json()['success']
        if ret2.json()['success']:
            print("域名:%-14s id:%-14s 清除缓存 结果:%s" % (ym,  value, jg))
        else:
            print("域名:%-14s id:%-14s 清除缓存 结果:%s" % (ym,  value, jg))
if __name__ == '__main__':
    # 密码
    org_name="DioXy1005..P@$.."
    # 账户id
    org_id="7a058d3d604990c35840275db3cacffe"
    #CF接口URL
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {'content-type': 'application/json',
               'X-Auth-Key': '6edfe72f5054d3e744c057c53ecedcf5b6edd',# 秘钥
               'X-Auth-Email': 'kyle90538@gmail.com'} #账号
    # 解析的ip
    host = "45.159.57.5"
    # 要解析的类型
    lists=['@','m','www']
    #证书CNAME,不需要的时候就使用空列表
    sslist = []
    #sslist=["_6cc55a9c7c1a40c72907dfbfef79ee61",'65c766ff8b831c926f7e8f3111d6fe5e.1e63f3020888f9099d282b4babb2c2a1.oc813ec20212979.sectigo.com']
    #启动CF证书的开关
    # SSL/TLS 加密模式valid values: off, flexible, full, strict
    # SSL/TLS 加密模式     有效值：关闭，灵活，完整，严格
    ## 始终使用HTTPS设置
    ## value:off 关闭 on 开启
    listssl=["strict","on"]
    #开始执行脚本,添加域名解析只用CreateCf
    #CreateCf(url,headers,host,org_name,org_id,lists,sslist)
    # 这个是修改https开关 和 修改是否启用CF证书的
    #PathSsl(url, headers, listssl)
    Clean_purge_everything() #这个是清除域名的所有缓存