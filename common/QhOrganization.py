# 期货机构的爬虫页面
import requests, sys, time, random, urllib.request
from lxml import etree
from dao import NewsDbUtli
from retrying import retry

# 初始化数据库 创建新闻表
NewsDbUtli.createNewsTable()

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
        content = htmlContent.xpath('.//div[@class="main"]')[1]
        orglists = []
        type = ""
        for div in content:

            if div.xpath('.//a[@class="blacklink"]') != None and len(div.xpath('.//a[@class="blacklink"]')) > 0:
                type = div.xpath('.//a[@class="blacklink"]')[0].text

            if div.xpath('.//div[@class="cmname"]') != None and len(div.xpath('.//div[@class="cmname"]')) > 0:
                orgContent = div.xpath('.//div[@class="cmname"]')
                for topDiv in orgContent:
                    org = {}
                    name = topDiv.xpath("./span/a")[0].text
                    href = str(topDiv.xpath("./span/a/@href")[0])
                    org["type"] = type
                    org["name"] = name
                    org["href"] = baseUrl + href
                    orglists.append(org)
                    print(type)

            if div.xpath('.//div[@class="tap2"]') != None and len(div.xpath('.//div[@class="tap2"]')) > 0:
                orgContent = div.xpath('.//div[@class="tap2"]')[0]
                for bomDiv in orgContent:
                    org = {}
                    href = str(bomDiv.xpath("@href")[0])
                    name = bomDiv.text
                    org["type"] = type
                    org["name"] = name
                    org["href"] = baseUrl + href
                    orglists.append(org)

                print(type)

        for org in orglists:
            getDetailInfo(org)


def getDetailInfo(org):
    href = org["href"]
    htmlContent = etree.HTML(parse_url(href))
    if htmlContent.xpath('.//div[@class="content_main"]') != None and len(
            htmlContent.xpath('.//div[@class="content_main"]')) > 0:

        # 处理图片 2处理资讯
        content = htmlContent.xpath('.//div[@class="content_main"]')[0]
        divInfo = content.xpath('.//div[@class="ltitle_logo"]')[0]
        icon = str(divInfo.xpath("./img/@src")[0])

        descInfo = content.xpath('.//div[@class="lcontent"]')[0]
        desc = descInfo.xpath("./span")[0].text
        org["icon"] = icon
        org["desc"] = desc

        newsList = content.xpath('.//ul/li')
        count = 0
        for news in newsList:
            count += 1
            if count > 12:
                return
            newsHref = str(news.xpath("./a/@href")[0])
            org["news_href"] = newsHref
            newstitle = news.xpath("./a")[0].text
            org["news_title"] = newstitle
            newsTime = news[1].text
            org["news_time"] = newsTime
            time.sleep(2)
            detailContent = etree.HTML(parse_url(newsHref))

            if detailContent.xpath('.//div[@class="Body"]') != None and len(
                    detailContent.xpath('.//div[@class="Body"]')) > 0:
                content = str(detailContent.xpath("string(.//div[@class='Body'])"))
                org["news_content"] = content
                NewsDbUtli.insertOrganizationNews(org["name"].strip(), org["icon"].strip(), org["type"].strip(),
                                                  org["desc"].strip(), org["news_time"].strip(),
                                                  org["news_title"].strip(), org["news_content"].strip(), "")


NewsDbUtli.createOrganizationTable()
getOrganizations()
