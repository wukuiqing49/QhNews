# 期货资讯爬虫启动页面

from dao import NewsDbUtli
from common import QhNews

# 初始化数据库 创建新闻表
NewsDbUtli.createNewsTable()
# 爬取 期货资讯
QhNews.getQhNews()
