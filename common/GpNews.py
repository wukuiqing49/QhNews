# 期货机构的爬虫页面

import time
from lxml import etree
from dao import GpDbUtli
from utils import UrlUtil

# 初始化数据库 创建新闻表
GpDbUtli.createGpNewsTable()
baseUrl = "http://finance.eastmoney.com/yaowen.html"

# 获取机构的数据
def getGpListNews(type, url):
    htmlContent = etree.HTML(UrlUtil.parse_url(url))
    if htmlContent.xpath(".//div[@class='repeatList']") != None and len(
            htmlContent.xpath(".//div[@class='repeatList']")) > 0 and htmlContent.xpath(".//div[@class='repeatList']")[
        0].xpath('.//ul/li') != None:
        content = htmlContent.xpath(".//div[@class='repeatList']")[0].xpath('.//ul/li')
        orglists = []
        for div in content:
            org = {}
            href = str(div.xpath('.//p[@class="title"]')[0].xpath('.//a/@href')[0])
            org["href"] = href
            if len(div.xpath('.//div/a/img/@src')) > 0:
                icon = str(div.xpath('.//div/a/img/@src')[0])
                org["icon"] = 'http:' + icon
            else:
               org["icon"] = ""
            title = div.xpath('.//p[@class="title"]')[0].xpath('.//a')[0].text
            org["title"] = title
            desc = div.xpath('.//p[@class="info"]')[0].text
            org["desc"] = desc
            time = div.xpath('.//p[@class="time"]')[0].text
            org["time"] = time
            org["type"] = type
            orglists.append(org)

        for org in orglists:
            getDetailInfo(org)


def getDetailInfo(org):
    time.sleep(2)
    href = org["href"]
    detailContent = etree.HTML(UrlUtil.parse_url(href))
    if detailContent.xpath('.//div[@class="Body"]') != None and len(
            detailContent.xpath('.//div[@class="Body"]')) > 0:
        content = str(detailContent.xpath("string(.//div[@class='Body'])"))
        # org["news_content"] = content
        GpDbUtli.insertGpNews(org["title"].strip(), org["icon"].strip(), org["type"].strip(), org["desc"].strip(),
                              content.strip(), org["time"].strip())

def getNewsType():
    htmlContent = etree.HTML(UrlUtil.parse_url(baseUrl))
    typs = []

    base = "http://finance.eastmoney.com"
    if len(htmlContent.xpath('.//ul[@id="articleTabs"]')) > 0:
        ul = htmlContent.xpath('.//ul[@id="articleTabs"]')[0]
        for li in ul:
            type = {}
            type["type"] = li.xpath('.//a')[0].text
            type["href"] = base+str(li.xpath('.//a/@href')[0])
            typs.append(type)

        for type in typs:
            getGpListNews(type["type"], type["href"])

getNewsType()

