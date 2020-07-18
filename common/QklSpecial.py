# 期货机构的爬虫页面
import json, time
from lxml import etree
from dao import QklDbUtli
from utils import UrlUtil

# 初始化区块链资讯表
QklDbUtli.createQklNewsTable()
QklDbUtli.createQkl7X24NewsTable()
QklDbUtli.createQklAuthorNesTable()

cProxy = {'http': '177.69.203.66:3128'}

typeNum = [0, 21, 22, 23, 25, 27, 29, 30, 32]
baseUrl = "https://www.55coin.com/index/article/search.html?cat_id=%d&page=1"
newsUrl = "https://www.55coin.com/article/%s.html"
newsAuthorListUrl = "https://www.55coin.com/column.html"
newsAuthorDetailUrl = "https://www.55coin.com/author/%s.html"
news24Url = 'https://www.55coin.com/index/flash/search_query.html?cat_id=0&page=1'
news7x24Detail = 'https://www.55coin.com/flash/%s.html'
baseUrlNews = "https://www.55coin.com/index/article/search.html?flash_cat_id=0&page=1"

header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'www.55coin.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Referer': "https://www.55coin.com/",
    'Cookie': 'PHPSESSID=t656r2b281pamja58naeepbu8t'
}


# 获取类型资讯的数据
def getNewsListByType(url):
    content = UrlUtil.parse_url_get_proxy(url)
    content = json.loads(content)
    list = content['list']
    listNews = []
    newsType = []

    for data in list:
        news = {}

        # 文章id
        article_id = data['article_id']
        news['newsId'] = str(article_id)
        # 作者id
        editor_id = data['editor_id']
        news['authorId'] = str(editor_id)

        # 作者名字
        author_name = data['author_name']
        news['authorName'] = author_name
        # 标题
        title = data['title']
        news['newsTitle'] = title
        # 简介
        brief = data['brief']
        news['newsDesc'] = brief
        # 图片
        rectangle_img = data['rectangle_img']
        news['newsIcon'] = rectangle_img
        # 类型
        cat_name = data['cat_name']
        news['newsType'] = cat_name
        if cat_name not in newsType:
            newsType.append(cat_name)
        # 查看数
        show_total = data['show_total']
        news['newsWatch'] = str(show_total)
        # 时间
        add_time = data['add_time']
        news['newsTime'] = str(add_time)
        if len(listNews) < 13:
            listNews.append(news)
    # 获取json数据

    return listNews


def getNewsDetail(news):
    time.sleep(2)
    url = newsUrl % (news['newsId'])
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(url))

    if len(
            htmlContent.xpath('.//div[@class="content"]')) > 0:
        detail = str(htmlContent.xpath("string(.//article[@class='article-content'])"))

        news['newsDetail'] = detail
        QklDbUtli.insertQklNews(news)
        print(news['newsTitle'])


def getNewsListByTag():
    newsList = []
    for news in typeNum:
        if news == 0:
            list = getNewsListByType(baseUrlNews)
        else:
            list = getNewsListByType(baseUrl % (news))
        for new in list:
            newsList.append(new)

        for news in newsList:
            getNewsDetail(news)


def getNews7x24Detail(news):
    time.sleep(2)
    url = news7x24Detail % (news['newsId'])
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(url))

    if len(
            htmlContent.xpath('.//div[@class="content"]')) > 0:
        detail = str(htmlContent.xpath("string(.//article[@class='article-content'])"))
        news['newsDetail'] = detail
        QklDbUtli.insert7x24News(news)
        print(news['newsTitle'])


# 获取机构的数据
def getNewsList24():
    content = UrlUtil.parse_url_get_proxy(news24Url)
    content = json.loads(content)
    list = content['list']
    listNews = []
    newsType = []

    for data in list:
        news = {}
        # 文章id
        article_id = data['flash_id']
        news['newsId'] = str(article_id)
        # 标题
        title = data['title']
        news['newsTitle'] = title
        # 简介
        brief = data['brief']
        news['newsDesc'] = brief
        news['newsType'] = '24小时'
        # 时间
        add_time = data['add_time']
        news['newsTime'] = str(add_time)
        rise = data['rise']
        news['newsSupport'] = str(rise)
        fall = data['fall']
        news['newsSupportNo'] = str(fall)
        listNews.append(news)

    # 获取json数据
    for news in listNews:
        getNews7x24Detail(news)


def getAuthorNewsDetails(author):
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(author['href']))
    if len(
            htmlContent.xpath('.//div[@class="content"]')) > 0:
        detail = str(htmlContent.xpath("string(.//article[@class='article-content'])"))
        author['newsDetail'] = detail.strip()
        QklDbUtli.insertQklAuthorsNews(author)
        print("标题:"+author['newsTitle'])


def getAuthorDetail(author):
    time.sleep(2)
    url = newsAuthorDetailUrl % (author['authorId'])

    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(url))

    if len(
            htmlContent.xpath('.//article[@class="excerpt"]')) > 0:
        ulcontent = htmlContent.xpath('.//article[@class="excerpt"]')
        authorNews = []
        author['authorFuns'] = htmlContent.xpath('.//ul[@class="data"]/li/span')[4].text
        author['authorNews'] = htmlContent.xpath('.//ul[@class="data"]/li/span')[0].text
        for news in ulcontent:
            if len(authorNews) < 16:
                authornew = {}

                authornew['authorFuns'] = author['authorFuns']
                authornew['authorNews'] = author['authorNews']
                authornew['authorId'] = author['authorId']
                authornew['authorName'] = author['authorName']
                authornew['authorDesc'] = author['authorDesc']

                authornew['authorName'] = author['authorName']
                authornew['authorIcon'] = author['authorIcon']
                authornew['authorSupport'] = author['authorSupport']

                authornew['newsTitle'] = str(news.xpath('./header/h2/a/@title')[0])
                if news.xpath('./p')[0].text is None:
                    authornew['newsDesc'] = ''
                else:
                    authornew['newsDesc'] = news.xpath('./p')[0].text
                authornew['newsIcon'] = str(news.xpath('./div/a/img/@src')[0])
                # 类型
                authornew['newsType'] = news.xpath('./header/a')[0].text
                authornew['href'] = "https://www.55coin.com" + news.xpath('./div/a/@href')[0]
                authornew['newsId'] = "".join(list(filter(str.isdigit, str(news.xpath('./div/a/@href')[0]))))
                # 查看数
                authornew['newsWatch'] = str(news.xpath('.//span[@class="muted none"]/text()')[0])
                authornew['newsTime'] = str(news.xpath('.//span[@class="muted"]/text()')[1])
                authorNews.append(authornew)

        for news in authorNews:
            print("")
            getAuthorNewsDetails(news)


def getAuthorList():
    htmlContent = etree.HTML(UrlUtil.parse_url_get_proxy(newsAuthorListUrl))

    if len(
            htmlContent.xpath('.//ul[@id="column_rank"]')) > 0:
        ulcontent = htmlContent.xpath('.//ul[@id="column_rank"]')[0]
        authorList = []
        for data in ulcontent:
            author = {}
            author['authorId'] = str(data.xpath('./a/@user_id')[0])
            author['authorName'] = data.xpath('./a/div/strong')[0].text

            if data.xpath('./a/div/span')[0].text is None:
                author['authorDesc'] = ""
            else:
                author['authorDesc'] = data.xpath('./a/div/span')[0].text

            author['authorIcon'] = str(data.xpath('./a/img/@src')[0])
            author['authorSupport'] = str(data.xpath('./div')[0].text)
            authorList.append(author)

        for author in authorList:
            getAuthorDetail(author)



# 7x24
# getNewsList24()
# 区块链资讯
# getNewsListByTag()
# 作者
# getAuthorList()
