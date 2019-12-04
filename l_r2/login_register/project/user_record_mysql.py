import pymysql
from pymysql import InternalError
import project.app
from datetime import datetime

#创建数据库中的用户信息表
def record_create(userId,inputText,tulingRespose,time1,time2):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    #cursor.execute("DROP TABLE IF EXISTS record")3
    try:
        sql = """CREATE TABLE record(
                 ID int(5) NOT NULL auto_increment,#以自增序列为主键
                 USERID VARCHAR(10),
                 INPUTTEXT VARCHAR(50),
                 TULINGRESPOSE VARCHAR(50),
                 TIME1 DATETIME,
                 TIME2 DATETIME,
                 primary key(ID)
                 ) default charset='utf8'"""
        cursor.execute(sql)
    except InternalError:#若报表已经存在的错误则直接插入,否则先创建表再插入
        pass
    record_insert(userId,inputText,tulingRespose,time1,time2)
    db.close()

#给数据库中的用户信息表插入数据
def record_insert(userId,inputText,tulingRespose,time1,time2):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO record(USERID,INPUTTEXT,TULINGRESPOSE,TIME1,TIME2)VALUES ('%s','%s','%s','%s','%s')"%(userId,inputText,tulingRespose,time1,time2)
    #print(sql)
    cursor.execute(sql)  # 执行sql语句
    db.commit()  # 提交到数据库执行
    db.rollback()  # 如果发生错误则回滚
    db.close()

#删除数据库用户信息表中的某个记录
def record_delete(userId,inputText,tulingRespose):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "DELETE FROM record WHERE USERID='%s'"%userId
    db.commit()
    db.rollback()
    db.close()

#更新数据库的某些记录
def record_update(userId,inputText,tulingRespose):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE record SET INPUTTEXT=INPUTTEXT+'%s',TULINGRESPOSE=TULINGRESPOSE+'%s' WHERE USERID='%s'" % (inputText,tulingRespose,userId)
    cursor.execute(sql)
    db.commit()
    db.rollback()
    db.close()

#查询数据库某表中的某一记录内容
def record_query(userId):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM record WHERE USERID='%s'" % (userId)
    try:
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录元组
        #print(results)
    except:
        print("Error: unable to fetch data")
    db.close()
    return results

