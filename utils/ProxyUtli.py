# 代理帮助类
import requests, sys, time, json
import telnetlib
from utils import UrlUtil
from retrying import retry
# 代理服务器 的git 地址
# https://github.com/jiangxianli/ProxyIpLib
# 获取 代理地址的服务器接口地址
proxyServicePath = 'https://ip.jiangxianli.com/api/proxy_ips?page=1&country=中国&order_by="validated_at"'
proxyServicePathOne = 'https://ip.jiangxianli.com/api/proxy_ip?country=%E4%B8%AD%E5%9B%BD'


# 获取代理服务器地址 多个代理
def getProxys():
    content = UrlUtil.parse_url_get(proxyServicePath)
    content = json.loads(content)
    proxyList = []
    if content['data'] != None:
        for itemBean in content['data']['data']:
            proxy = {}
            proxy[itemBean['protocol']] = itemBean['ip'] + ':' + itemBean['port']
            proxyList.append(proxy)
    else:
        return ""
    return proxyList


def getProxy():
    content = UrlUtil.parse_url_get(proxyServicePathOne)
    content = json.loads(content)
    proxy = {}
    proxy[content['data']['protocol']] = content['data']['ip'] + ':' + content['data']['port']
    return proxy
# 处理重置的逻辑
@retry(stop_max_attempt_number=5)
def checkProxy(ip,port):
    try:
        telnetlib.Telnet(ip, port, timeout=5)
        return True
    except:
        return False

