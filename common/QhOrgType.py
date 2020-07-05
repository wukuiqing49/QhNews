# 期货机构的爬虫页面
import requests, sys, time, random, urllib.request
from lxml import etree
from dao import NewsDbUtli
from dao import GpDbUtli
from retrying import retry

# 初始化数据库 创建新闻表

GpDbUtli.createGpOrganizationTable()

baseUrl = "https://jigou.eastmoney.com"

defulProxies = {'https': '58.244.59.214:8080', 'https': '49.51.51.85:5379'}

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'jigou.eastmoney.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Referer': "https://jigou.eastmoney.com/futures/anliangqihuo",
    'Cookie': 'st_si=40687291001908; qgqp_b_id=fa38475769b5c9ee0435fa8e503f042e; waptgshowtime=2020627; cowCookie=true; st_asi=delete; st_pvi=22083436054373; st_sp=2020-06-27%2011%3A36%3A32; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=61; st_psi=20200630141243365-113800302983-0863240548'
}


@retry(stop_max_attempt_number=10)
def parse_url(url):
    session = requests.session()
    response = session.get(url=baseUrl, timeout=10)
    response.encoding = response.apparent_encoding
    response = requests.get(url, timeout=5)
    response.encoding = response.apparent_encoding
    return response.text


# 获取机构的数据
def getOrganizations():
    htmlContent = etree.HTML(parse_url(baseUrl))
    if htmlContent.xpath("/html/body/div[1]/div[4]") != None:
        content = htmlContent.xpath('.//div[@class="content_header"]')
        for div in content:

            if div.xpath('.//a[@class="blacklink"]') != None and len(div.xpath('.//a[@class="blacklink"]')) > 0:
                type = div.xpath('.//a[@class="blacklink"]')[0].text
                GpDbUtli.insertGpOrgType(type)





getOrganizations()
