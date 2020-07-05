# 资讯数据库操作工具
import sqlite3

from os import path
from utils import pathutil
from utils.pathutil import Pathutil

PathUtil = Pathutil()

dbName = PathUtil.rootPath + "/gp_news.sqlite3"


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
def createGpNewsTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS qh_news
              (id INTEGER PRIMARY KEY autoincrement,
              news_title TEXT,
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
def insertGpNews(title, desc, time, typs, href, src, content):
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO qh_news VALUES (?,?, ?, ?, ?, ?, ?, ?)"

    cur.execute(sql, (None, title, time, desc, typs, content, src, href))
    con.commit()
    cur.close()
    con.close()


# 创建机构表
def createOrganizationTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS qh_organization_news
              (id INTEGER PRIMARY KEY autoincrement,
               o_name TEXT,
               o_icon TEXT,
               o_type TEXT,
               o_desc TEXT,
               o_news_time TEXT,
               o_news_title TEXT,
               o_news_detail TEXT,
               o_news_icon TEXT)
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


# 插入 机构数据以及机构新闻
def insertOrganizationNews(o_name, o_icon, o_type, o_desc, o_news_time, o_news_title, o_news_detail, o_news_icon):
    print(o_name + ":" + o_news_title)
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO qh_organization_news VALUES (?,?,?, ?, ?, ?, ?, ?, ?)"

    cur.execute(sql, (None, o_name, o_icon, o_type, o_desc, o_news_time, o_news_title, o_news_detail, o_news_icon))
    con.commit()
    cur.close()
    con.close()


# 创建机构表
def createGpNewsTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS gp_news
              (id INTEGER PRIMARY KEY autoincrement,
                gp_title TEXT,
                gp_icon TEXT,
                gp_type TEXT,
                gp_desc TEXT,
                gp_detail TEXT,
                gp_time TEXT)
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


# 插入 股票数据
def insertGpNews(gp_title, gp_icon, gp_type, gp_desc, gp_detail, gp_time):
    print(gp_type + ":" + gp_title + " " + gp_time)
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO gp_news VALUES (?,?,?, ?, ?, ?, ?)"
    cur.execute(sql, (None, gp_title, gp_icon, gp_type, gp_desc, gp_detail, gp_time))
    con.commit()
    cur.close()
    con.close()


# 创建热评
def createGpCommonNewsTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS gp_common_news
              (id INTEGER PRIMARY KEY autoincrement,
                gp_title TEXT,
                gp_icon TEXT,
                gp_type TEXT,
                gp_desc TEXT,
                gp_detail TEXT,
                gp_time TEXT)
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


# 插入 股票数据
def insertGpCommonNews(gp_title, gp_icon, gp_type, gp_desc, gp_detail, gp_time):
    print(gp_type + ":" + gp_title + " " + gp_time)
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO gp_common_news VALUES (?,?,?, ?, ?, ?, ?)"
    cur.execute(sql, (None, gp_title, gp_icon, gp_type, gp_desc, gp_detail, gp_time))
    con.commit()
    cur.close()
    con.close()


# top新闻
def createGpTpTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS gp_top_news
              (id INTEGER PRIMARY KEY autoincrement,
                gp_title TEXT,
                gp_icon TEXT,
                gp_type TEXT,
                gp_detail TEXT)
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


# 插入 股票数据
def insertGpTopNews(gp_title, gp_icon, gp_type, gp_detail):
    print(gp_type + ":" + gp_title + " ")
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO gp_top_news VALUES (?,?,?, ?, ?)"
    cur.execute(sql, (None, gp_title, gp_icon, gp_type, gp_detail))
    con.commit()
    cur.close()
    con.close()


# 机构类型
def createGpOrganizationTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS gp_org
              (id INTEGER PRIMARY KEY autoincrement,
                gp_name TEXT)
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

# 插入 股票数据
def insertGpOrgType(orgName):
    print(orgName + ":")
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO gp_org VALUES (?,?)"
    cur.execute(sql, (None, orgName))
    con.commit()
    cur.close()
    con.close()
