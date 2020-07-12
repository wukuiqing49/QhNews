import requests, sys, time, random, urllib.request
from retrying import retry
from utils import ProxyUtli

# # 代理数据
cProxy = {'http': '177.69.203.66:3128'}


# 处理重置的逻辑
@retry(stop_max_attempt_number=10)
def parse_url(url):
    # session = requests.session()
    # response = session.get(url=baseUrl, timeout=10)
    # response.encoding = response.apparent_encoding
    response = requests.get(url, timeout=5)
    response.encoding = response.apparent_encoding
    return response.text


@retry(stop_max_attempt_number=10)
def parse_url_get(url):
    session = requests.session()
    response = session.get(url=url, timeout=10)
    response.encoding = response.apparent_encoding
    # response = requests.get(url, timeout=5)
    response.encoding = response.apparent_encoding
    return response.text


def parse_url_post(url, m_header, defulProxies):
    session = requests.session()
    response = session.post(url=url, timeout=10, header=m_header, proxies=defulProxies, verify=False)
    response.encoding = response.apparent_encoding
    response.encoding = response.apparent_encoding
    return response.text


# 代理请求 获取json数据
@retry(stop_max_attempt_number=10)
def parse_url_get_proxy(url):
    http = cProxy['http'].split(':')
    check = ProxyUtli.checkProxy(http[0], http[1])
    if check == True:
        response = requests.get(url=url, proxies=cProxy)
        response.encoding = response.apparent_encoding
    else:
        cProxy['http'] = ProxyUtli.getProxy()['http']
        response = requests.get(url=url, proxies=cProxy)
        response.encoding = response.apparent_encoding

    return response.text
