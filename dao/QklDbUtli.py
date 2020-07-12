# 区块链资讯数据库操作工具
import sqlite3
from utils.pathutil import Pathutil

PathUtil = Pathutil()

dbName = PathUtil.rootPath + "/qkl_news.sqlite3"


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


# 创建区块链新闻表
def createQklNewsTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS qkl_news
              (id INTEGER PRIMARY KEY autoincrement,
               news_id TEXT,
               news_author_name TEXT,
               news_author_id TEXT,
               news_author_icon TEXT,
               news_author_desc TEXT,
               news_watch TEXT,
               news_time TEXT,
               news_title TEXT,
               news_desc TEXT,
               news_type TEXT,
               news_detail TEXT,
               news_icon TEXT)
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

# 创建区块链新闻表
def createQklTagTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS qkl_news_tag
              (id INTEGER PRIMARY KEY autoincrement,
               tag_name TEXT)
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

def insertTag(tagName):

    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO qkl_news_tag VALUES (?,?)"
    cur.execute(sql, (None,
                      tagName))
    con.commit()
    cur.close()
    con.close()

# 创建区块链新闻表
def createQklAuthorNesTable():
    con = getDbconnect()

    sql = '''
          CREATE TABLE IF NOT EXISTS qkl_author_news
              (id INTEGER PRIMARY KEY autoincrement,
               news_id TEXT,
               news_author_name TEXT,
               news_author_id TEXT,
               news_author_icon TEXT,
               news_author_desc TEXT,
               news_author_support TEXT,
               news_author_funs TEXT,
               news_author_news TEXT,
               news_watch TEXT,
               news_time TEXT,
               news_title TEXT,
               news_desc TEXT,
               news_type TEXT,
               news_detail TEXT,
               news_icon TEXT)
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


# 保存 区块链 新闻数据
def insertQklAuthorsNews(qklNews):
    con = getDbconnect()
    cur = con.cursor()
    if 'authorDesc' not in qklNews:
        qklNews['authorDesc'] = ""
    if 'newsDesc' not in qklNews:
        qklNews['newsDesc'] = qklNews['newsTitle']
    if 'newsTitle' not in qklNews:
        qklNews['newsTitle'] = ""

    sql = "INSERT INTO qkl_author_news VALUES (?,?,?,?,?, ?,?, ?, ?, ?, ?, ?,?,?,?,?)"
    cur.execute(sql, (None,
                      qklNews['newsId'],
                      qklNews['authorName'].strip(),
                      qklNews['authorId'],
                      qklNews['authorIcon'],
                      qklNews['authorDesc'].strip(),

                      qklNews['authorSupport'].strip(),
                      qklNews['authorFuns'].strip(),
                      qklNews['authorNews'].strip(),

                      qklNews['newsWatch'],
                      qklNews['newsTime'],
                      qklNews['newsTitle'].strip(),
                      qklNews['newsDesc'].strip(),
                      qklNews['newsType'].strip(),
                      qklNews['newsDetail'].strip(),
                      qklNews['newsIcon'].strip()))
    con.commit()
    cur.close()
    con.close()  # 保存 区块链 新闻数据


def insertQklNews(qklNews):
    if 'newsDetail' not in qklNews or qklNews['newsDetail'] is None:
        qklNews['newsDetail'] = ""
    if 'authorIcon' not in qklNews or qklNews['authorIcon'] is None:
        qklNews['authorIcon'] = ""
    if 'authorDesc' not in qklNews or qklNews['authorDesc'] is None:
        qklNews['authorDesc'] = ""
    if 'newsDesc' not in qklNews or qklNews['newsDesc'] is None:
        qklNews['newsDesc'] = ""
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO qkl_news VALUES (?,?, ?,?, ?, ?, ?, ?, ?,?,?,?,?)"
    cur.execute(sql, (None,
                      qklNews['newsId'],
                      qklNews['authorName'].strip(),
                      qklNews['authorId'],
                      qklNews['authorIcon'],
                      qklNews['authorDesc'].strip(),
                      qklNews['newsWatch'],
                      qklNews['newsTime'],
                      qklNews['newsTitle'].strip(),
                      qklNews['newsDesc'].strip(),
                      qklNews['newsType'].strip(),
                      qklNews['newsDetail'].strip(),
                      qklNews['newsIcon'].strip()))
    con.commit()
    cur.close()
    con.close()


# 创建新闻表
def createQkl7X24NewsTable():
    con = getDbconnect()
    sql = '''
          CREATE TABLE IF NOT EXISTS qkl_seven_news
              (id INTEGER PRIMARY KEY autoincrement,
               news_id TEXT,
               news_time TEXT,
               news_title TEXT,
               news_desc TEXT,
               news_type TEXT,
               news_detail TEXT,
               news_support TEXT,
               news_support_no TEXT )
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


# 保存 7x24 新闻数据
def insert7x24News(qklNews):
    if 'newsDetail' not in qklNews:
        qklNews['newsDetail'] = ""
    con = getDbconnect()
    cur = con.cursor()
    sql = "INSERT INTO qkl_seven_news VALUES (?, ?, ?, ?, ?,?,?,?,?)"
    cur.execute(sql, (None,
                      qklNews['newsId'],
                      qklNews['newsTime'],
                      qklNews['newsTitle'].strip(),
                      qklNews['newsDesc'].strip(),
                      qklNews['newsType'].strip(),
                      qklNews['newsDetail'].strip(),
                      qklNews['newsSupport'].strip(),
                      qklNews['newsSupportNo'].strip()
                      ))
    con.commit()
    cur.close()
    con.close()
