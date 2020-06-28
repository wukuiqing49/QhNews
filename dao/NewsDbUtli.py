# 资讯数据库操作工具
import sqlite3

from os import path
from utils import pathutil
from utils.pathutil import Pathutil

PathUtil = Pathutil()

dbName = PathUtil.rootPath+"/qhzx.sqlite3"


# 打开数据库
# con = sqlite3.connect("qh.sqlite3")
# 获取游标
# cur = con.cursor()
# 执行sql
# cur.execute("SELECT title FROM exam")
# fetchall()获取所有数据
# print(cur.execute("SELECT * FROM exam").fetchall())

def getDbconnect():
    # 打开数据库
    con = sqlite3.connect(dbName)
    return con


def getDbCursor(con):
    # 获取游标
    cur = con.cursor()
    return cur


def getDbCursor():
    # 获取游标
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    return cur


# 创建新闻表
def createNewsTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS qh_news
              (news_title TEXT,
               news_time TEXT,
               news_desc TEXT,
               news_type TEXT,
               news_detail TEXT,
               news_src TEXT,
               news_href TEXT)
          '''
    try:

        # 主要就是上面的语句
        con.execute(sql)
    except:
        print
        "Create table failed"
        return False
    con.execute(sql)
    con.commit()


# 保存 新闻数据
def insertNews(title, desc, time, typs, href, src, content):
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO qh_news VALUES (?, ?, ?, ?, ?, ?, ?)"

    cur.execute(sql, (title, time, desc, typs, content, src, href))
    con.commit()
    cur.close()
    con.close()