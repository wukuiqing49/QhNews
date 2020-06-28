# 期货资讯爬虫启动页面
import sys
import requests, sys, time, random, urllib.request
from lxml import etree
from dao import NewsDbUtli

# 初始化数据库 创建新闻表
NewsDbUtli.createNewsTable()

baseUrl = "http://futures.eastmoney.com/a/cqhdd.html"

defulProxies = {'https': '58.244.59.214:8080', 'https': '49.51.51.85:5379'}

header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Host": "futures.eastmoney.com",
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    "Referer": "http://futures.eastmoney.com/a/cqhdd.html",
    "Cookie": "qgqp_b_id=fa38475769b5c9ee0435fa8e503f042e; st_si=40687291001908; st_asi=delete; st_pvi=22083436054373; st_sp=2020-06-27%2011%3A36%3A32; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=9; st_psi=20200627120513158-113200301326-8579988931"
}


def getTypeNews(newsUrl: str, mType: str):
    session = requests.session()
    response = session.get(url=newsUrl, timeout=(3, 7), proxies=defulProxies, verify=False)
    response.encoding = response.apparent_encoding
    htmlContent = etree.HTML(response.text)
    if htmlContent.xpath("//*[@id='newsListContent']")[0] != None and len(
            htmlContent.xpath("//*[@id='newsListContent']")[0]) > 0:
        listNews = htmlContent.xpath("//*[@id='newsListContent']")[0]
        news = []
        for div in listNews:
            mNew = {}
            if len(div.xpath("./div")) >= 2:

                src = div.xpath("./div")[0].xpath('./a/img/@src')[0]
                if not str(src).startswith("http"):
                    src = div.xpath("./div")[0].xpath('./a/img/@src')[0]
                    mNew["src"] = "http:" + src
                href = div.xpath("./div")[0].xpath('./a/@href')[0]
                mNew["href"] = str(href)

                title = div.xpath("./div")[1].xpath("./p/a")[0].text
                mNew["title"] = title

                desc = div.xpath("./div")[1].xpath("./p")[1].text
                mNew["desc"] = desc

                time = div.xpath("./div")[1].xpath("./p")[2].text
                mNew["time"] = time
                mNew["typs"] = mType

            else:
                # src = div.xpath("./div")[0].xpath('./a/img/@src')[0]
                # if not str(src).startswith("http"):
                #     mNew = {}
                #     src = div.xpath("./div")[0].xpath('./a/img/@src')[0]
                #     mNew["src"] = "http:" + src
                mNew["src"] = ""
                href = div.xpath("./div")[0].xpath('./p/a/@href')[0]
                mNew["href"] = str(href)

                title = div.xpath("./div")[0].xpath("./p/a")[0].text
                mNew["title"] = title
                desc = div.xpath("./div")[0].xpath("./p")[1].text
                mNew["desc"] = desc

                time = div.xpath("./div")[0].xpath("./p")[2].text

                mNew["time"] = time
                mNew["typs"] = mType
            # response = session.get(url=href, timeout=(3, 7), proxies=defulProxies, verify=False)
            # response.encoding = response.apparent_encoding
            # htmlContent = etree.HTML(response.text)
            # if htmlContent.xpath("//*[@id='ContentBody']") != None:
            #    content= htmlContent.xpath("//*[@id='ContentBody']")
            #    mNew["content"] = str(content)
            NewsDbUtli.insertNews(mNew.get("title").strip(), mNew.get("desc").strip(), mNew.get("time").strip(),
                                  mNew.get("typs").strip(), mNew.get("href").strip(), mNew.get("src").strip(), "")
        print(news)


def getQhNews():
    newTypes = []

    mNew1 = {}
    mNew1["type"] = "期货首页"
    mNew1["href"] = "http://futures.eastmoney.com/a/cqhdd.html"
    newTypes.append(mNew1)
    mNew2 = {}
    mNew2["type"] = "期市聚焦"
    mNew2["href"] = "http://futures.eastmoney.com/a/cqsyw.html"
    newTypes.append(mNew2)
    mNew3 = {}
    mNew3["type"] = "焦点访问"
    mNew3["href"] = "http://futures.eastmoney.com/a/cjdgc.html"
    newTypes.append(mNew3)
    mNew4 = {}
    mNew4["type"] = "国内期货"
    mNew4["href"] = "http://futures.eastmoney.com/a/cqspl.html"
    newTypes.append(mNew4)
    mNew5 = {}
    mNew5["type"] = "外盘速递"
    mNew5["href"] = "http://futures.eastmoney.com/a/cwpsd.html"
    newTypes.append(mNew5)

    mNew6 = {}
    mNew6["type"] = "综合资讯"
    mNew6["href"] = "http://futures.eastmoney.com/a/czhzx.html"
    newTypes.append(mNew6)

    for typeInfo in newTypes:
        time.sleep(3)
        getTypeNews(typeInfo.get("href"), typeInfo.get("type"))

