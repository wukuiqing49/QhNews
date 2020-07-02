import requests, sys, time, random, urllib.request
from retrying import retry


# 处理重置的逻辑
@retry(stop_max_attempt_number=10)
def parse_url(url):
    # session = requests.session()
    # response = session.get(url=baseUrl, timeout=10)
    # response.encoding = response.apparent_encoding
    response = requests.get(url, timeout=5)
    response.encoding = response.apparent_encoding
    return response.text


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
