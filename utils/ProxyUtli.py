# 代理帮助类
import requests, sys, time, json
from utils import UrlUtil

# 代理服务器 的git 地址
# https://github.com/jiangxianli/ProxyIpLib
# 获取 代理地址的服务器接口地址
proxyServicePath = 'https://ip.jiangxianli.com/api/proxy_ips?page=1&country=中国&order_by="validated_at"'


# 获取代理服务器地址 多个代理
def getProxyUtil():
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

# getProxyUtil()
