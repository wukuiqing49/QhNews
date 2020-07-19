# 区块链首页 爬虫
import json, time
from lxml import etree
from dao import QklDbUtli
from utils import UrlUtil

baseUrl = 'https://www.55coin.com'
newsUrl = "https://www.55coin.com/article/%s.html"
QklDbUtli.createQklNewsTable()
QklDbUtli.createQklTagTable()


def getNewsDetail(news):
    time.sleep(2)
    url = newsUrl % (news['newsId'])
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(url))

    if htmlContent.xpath('.//div[@class="content-wrap"]') != None and len(
            htmlContent.xpath('.//div[@class="content"]')) > 0:
        detail = str(htmlContent.xpath("string(.//article[@class='article-content'])"))
        news['newsDetail'] = detail
        # 作者名字
        news['authorName'] = htmlContent.xpath('.//div[@class="meta"]/span')[1].text
        news['authorDesc'] = ""
        # 查看数
        news['newsWatch'] = "".join(list(filter(str.isdigit, str(htmlContent.xpath('.//span[@class="muted"]/text()')))))
        # 时间
        news['newsTime'] = htmlContent.xpath('.//div[@class="meta"]/time')[0].text
        QklDbUtli.insertQklNews(news)
        print(news['newsTitle'])


def getHomeInfo():
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(baseUrl))

    hotContent = htmlContent.xpath(".//ul[@class='article-list']")[0]
    hotList = []
    for hotNews in list(hotContent):
        news = {}
        # 文章id
        news['newsId'] = "".join(list(filter(str.isdigit, str(hotNews.xpath('./a/@href')[0]))))
        # 作者id
        news['authorId'] = ""
        # 作者名字
        news['authorName'] = ""

        news['authorDesc'] = ""
        # 标题
        if (len(hotNews.xpath('.//div[@class="tit"]')) > 0):
            news['newsTitle'] = hotNews.xpath('.//div[@class="tit"]')[0].text
        else:
            news['newsTitle'] = str(hotNews.xpath('.//div/a/@title')[0])

        # 简介
        news['newsDesc'] = ""
        # 图片
        news['newsIcon'] = str(hotNews.xpath('.//img/@src')[0])
        # 类型
        news['newsType'] = "hot"
        # 查看数
        news['newsWatch'] = ""
        # 时间
        news['newsTime'] = ""
        # 详情
        news['newsDetail'] = ""
        hotList.append(news)

    for news in hotList:
        getNewsDetail(news)


# 获取类型资讯的数据
def getNewsListByType(url, tag):
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(url))

    listContent = htmlContent.xpath('.//article[@class="excerpt"]')
    listNews = []

    for data in listContent:
        news = {}
        # 文章id
        article_id = "".join(list(filter(str.isdigit, str(data.xpath('.//a/@href')[0]))))
        news['newsId'] = str(article_id)
        # 作者id

        news['authorId'] = ""

        # 作者名字
        author_name = data.xpath('.//span[@class="muted"]')[0].text
        news['authorName'] = author_name
        news['authorDesc'] = ""
        news['authorIcon'] = ""
        # 标题
        title = data.xpath('./header/h2/a')[0].text
        news['newsTitle'] = title
        # 简介
        if data.xpath('./p') is None:
            news['newsDesc'] = ''
        else:
            news['newsDesc'] = data.xpath('./p')[0].text

        # 图片

        if len(data.xpath('./div/a/img/@src')) == 0 or data.xpath('./div/a/img/@src')[0] is None:
            news['newsIcon'] = ""
        else:
            rectangle_img = str(data.xpath('./div/a/img/@src')[0])
            news['newsIcon'] = rectangle_img
        # 类型

        news['newsType'] = tag
        # 查看数
        show_total = str(data.xpath('.//span[@class="muted none"]/text()')[0])
        news['newsWatch'] = str(show_total)
        # 时间
        add_time = data.xpath('.//span[@class="muted"]')[1].text
        news['newsTime'] = str(add_time)
        if len(listNews) < 13:
            listNews.append(news)
    # 获取json数据

    for news in listNews:
        getNewsTagDetail(news)


def getNewsTagDetail(news):
    time.sleep(2)
    url = newsUrl % (news['newsId'])
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(url))

    if len(
            htmlContent.xpath('.//div[@class="content"]')) > 0:
        detail = str(htmlContent.xpath("string(.//article[@class='article-content'])"))
        news['newsDetail'] = detail
        QklDbUtli.insertQklNews(news)
        print(news['newsTitle'])


def getTag():
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(baseUrl))
    tagContent = htmlContent.xpath('.//div[@class="d_tags"]/a')

    for tag in tagContent:
        url = baseUrl + str(tag.xpath('./@href')[0])
        QklDbUtli.insertTag(tag.text)
        # getNewsListByType(url, tag.text)


def getTagNews():
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(baseUrl))
    tagContent = htmlContent.xpath('.//div[@class="d_tags"]/a')

    for tag in tagContent:
        url = baseUrl + str(tag.xpath('./@href')[0])
        getNewsListByType(url, tag.text)

# getHomeInfo()
# getTag()
