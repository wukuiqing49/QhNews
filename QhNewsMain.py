# 期货资讯爬虫启动页面
from common import QklSpecial
from common import QkNewsHome


# 获取区块链新闻
def getQklNews():
    QkNewsHome.getHomeInfo()
    QkNewsHome.getTag()
    QkNewsHome.getTagNews()

    QklSpecial.getNewsList24()
    # 区块链资讯
    QklSpecial.getNewsListByTag()
    # 作者
    QklSpecial.getAuthorList()

# 机构数据
# NewsDbUtli.createOrganizationTable()
# getOrganizations()

# 初始化数据库 创建新闻表
# NewsDbUtli.createNewsTable()
# 爬取 期货资讯
# QhNews.getQhNews()

# 初始化数据库 创建热评
# GpDbUtli.createGpCommonNewsTable()
# getNewsType()

# 初始化数据库 top人物数据
# GpDbUtli.createGpTpTable()
# getNewsType("TopNews")

getQklNews()