import pymysql
from pymysql import InternalError
import project.app
from datetime import datetime
import re

#查询2018-2019未分方向时候的课程表(要实现将课程表的时间用正则表达式进行分割)
# str='1222_.dat_56'
# str1=re.findall(r'\d{1,2}',str) #就可以分割出所有的数字（最后一周）
# #下面得到最后一周
# last_week=str1[-1]  #56
#得到最后一周之后然后将本周是第几周传进去，看是否小于最后一周，小于的话，就说明属于这个周范围，即可用select语句筛选出今天的课程

def class_schedule_query(grade,class1,this_week,day):   #grade是用户所在的年级,class1是用户所在的班级,week是第几周,day是周几
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM class_schedule WHERE grade='%s' and class='%s' and day='%s'" % (grade, class1, day)
    try:
        cursor.execute(sql)  # 执行SQL语句
        results=cursor.fetchall()  # 获取所有记录元组
        result1=[]
        print(len(results))
        for i in range(len(results)):
            week_max = re.findall(r'\d{1,2}', results[i][2])[-1]
            week_min=re.findall(r'\d{1,2}', results[i][2])[0]
            if(int(week_min)<=int(this_week)<=int(week_max)):
                result1.append(results[i])
    except:
        print("Error: unable to fetch data")
    db.close()
    return result1


#查询2017级分方向之后的课程表
def class_schedule_query1(grade,this_week,day,direction):   #grade是用户所在的年级,class1是用户所在的班级,week是第几周,day是周几
    db = pymysql.connect(host='localhost',user='root',database='user_information',charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM class_schedule WHERE grade='%s' and day='%s' and direction='%s'" % (grade,day,direction)
    try:
        cursor.execute(sql)  # 执行SQL语句
        results=cursor.fetchall()  # 获取所有记录元组
        result1=[]
        print(len(results))
        for i in range(len(results)):
            week_max = re.findall(r'\d{1,2}', results[i][2])[-1]
            week_min=re.findall(r'\d{1,2}', results[i][2])[0]
            if(int(week_min)<=int(this_week)<=int(week_max)):
                result1.append(results[i])
    except:
        print("Error: unable to fetch data")
    db.close()
    return result1