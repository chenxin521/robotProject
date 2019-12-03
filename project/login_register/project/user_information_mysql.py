import pymysql
from pymysql import InternalError
import project.app
from datetime import datetime

#创建数据库中的用户信息表
def information_create(studentid,username,email,password):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    # cursor.execute("DROP TABLE IF EXISTS information")
    try:
        sql = """CREATE TABLE information(
                 STUDENTID CHAR(10) ,
                 USERNAME  VARCHAR(20),
                 EMAIL VARCHAR(20),
                 PASSWORD  VARCHAR(15),
                 primary key(STUDENTID))"""
        cursor.execute(sql)
    except InternalError:#若报表已经存在的错误则直接插入,否则先创建表再插入
        pass
    finally:
        information_insert(studentid,username,email,password)
    db.close()
    return 1

#给数据库中的用户信息表插入数据
def information_insert(studentid,username,email,password):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO information(STUDENTID,USERNAME,EMAIL,PASSWORD)VALUES ('%s','%s','%s','%s')"%(studentid,username,email,password)
    #print(sql)
    cursor.execute(sql)  # 执行sql语句
    db.commit()  # 提交到数据库执行
    db.rollback()  # 如果发生错误则回滚
    db.close()

#删除数据库用户信息表中的某个记录
def information_delete(username):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "DELETE FROM information WHERE USERNAME==username"
    db.commit()
    db.rollback()
    db.close()

#更新数据库的用户信息表
def information_update(username,new_password):
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE information SET password=new_password WHERE USERNAME='%s'" % username
    cursor.execute(sql)
    db.commit()
    db.rollback()
    db.close()

#查询用户信息表中的某一记录内容
def information_query(username):
    return_password=[]
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "SELECT PASSWORD FROM information WHERE USERNAME='%s'" % (username)
    try:
        cursor.execute(sql)  # 执行SQL语句
        results= cursor.fetchall()  # 获取所有记录元组
        return_password=results[0][0]
    except:
        print("Error: unable to fetch data")
    db.close()
    return return_password
