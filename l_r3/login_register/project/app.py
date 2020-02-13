#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, redirect,\
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json
import urllib.request
from project import user_information_mysql as informationMysql
from project import user_record_mysql as recordMysql
from project import hand_write_100 as hw
from project import class_schedule_mysql as scheduleMysql
from project import zyq
from project import map
from datetime import datetime
import pymysql
import datetime
import re
import numpy as np
import time
import math
import base64
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

#
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route("/test/",methods=['POST','GET'])
def test():
    return render_template('test.html')



##先留着
# @socketio.on('my_broadcast_event', namespace='/test')
# def test_broadcast_message(message):
#     print(message)
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': '您说的"' + message['data'] + '"我已经收到了', 'count': session['receive_count']},
#          broadcast=True)


# {'data': message['data'], 'count': session['receive_count']},


tuling='3d3fa6b66f72479eaa9c45be57b639e0'  #老师的
#tuling='e238e5b6de7545fc886720c0d175cb79'    #张琳的
#tuling= 'b9c94835bf924281b681248828c006d1'  #陈鑫的
api_url = "http://openapi.tuling123.com/openapi/api/v2"

tulinglist = ['3d3fa6b66f72479eaa9c45be57b639e0','e238e5b6de7545fc886720c0d175cb79','b9c94835bf924281b681248828c006d1']
counttuling = 0
gurl = '3d3fa6b66f72479eaa9c45be57b639e0'

@socketio.on('my_broadcast_event', namespace='/test')
def get_message(message):
    time1=datetime.datetime.now()
    global counttuling
    global gurl
    req = {
    "perception":
    {
        "inputText":
        {
            "text": message['data']
        },

        "selfInfo":
        {
            "location":
            {
                "city": "河北",
                "province": "石家庄",
                "street": "XXX"
            }
        }
    },
    "userInfo":
    {
        "apiKey": gurl,
        "userId": message['userId']
    }
    }
    req = json.dumps(req).encode('utf8')
    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)
    print(response_dic)
    # 询问某道菜怎么做时，直接返回url
    if "text" in response_dic['results'][0]['values']:
        results_text = response_dic['results'][0]['values']['text']
    elif "url" in response_dic['results'][0]['values']:
        results_text = response_dic['results'][0]['values']['url']
    # elif "怎么做" in message['data']:
    #     results_text = response_dic['results'][0]['values']['url']
    else:
        results_text="换一个问题吧！"


    if(results_text == '请求次数超限制！'):
        if(counttuling < len(tulinglist)):
            counttuling += 1
            gurl = tulinglist[counttuling]
            results_text = '出错了！请再次输入！'
        else:
            results_text = '亲，今日小软棉聊天次数已用完！但是亲仍可以继续查询课表和识别图片呦！欢迎明天再来哦~'




    session['receive_count'] = session.get('receive_count', 0) + 1
    time2 = datetime.datetime.now()


    if(message['check']!=""):
        emit('my_response',
             {'question': message['data'], 'username': message['check'], 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': results_text, 'count': session['receive_count']}
             )
        recordMysql.record_create1(message['check'], message['data'], results_text, time1, time2)
    else:
        emit('my_response',
             {'question': message['data'], 'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': results_text, 'count': session['receive_count']}
             )

@socketio.on('my_broadcast_table_event', namespace='/test')
def get_table_message(message):
    time1 = datetime.datetime.now()

    # 计算现在是第几周的代码
    today = datetime.date.today()
    date1 = time.strptime('2019-09-02', "%Y-%m-%d")
    date2 = time.strptime(str(today), "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    days_number = (date2 - date1).days
    #print(type(days_number))
    #得到这周是多少周
    this_week = math.ceil(days_number / 7)
    print(type(this_week))
    #print(days_number, this_week)
    # 这是2017级查询
    if re.search('\w+方向', message['data']):
        if re.search('\d\d\d\d级', message['data']) and re.search('星期\D{1}', message['data']):
            grade = re.findall('\d\d\d\d级', message['data'])
            # class1 = re.findall('\d-\d班', message['data'])
            day = re.findall('星期\D', message['data'])
            direction = re.findall('[H,J,软，人]\w+方向', message['data'])
            results_text = scheduleMysql.class_schedule_query1(grade[0], str(this_week), day[0],
                                                               direction[0])

    # #这是2018和2019级查询
    elif re.search('\d\d\d\d级', message['data']) and re.search('[1-8]班', message['data']) and re.search('星期\D{1}',message['data']):
        grade = re.findall('\d\d\d\d级', message['data'])
        class1 = re.findall('[1-8]班', message['data'])
        # week = re.findall('\d{1,2}周', message['data'])
        day = re.findall('星期\D', message['data'])
        results_text = scheduleMysql.class_schedule_query(grade[0], class1[0], str(this_week), day[0])

    session['receive_count'] = session.get('receive_count', 0) + 1
    time2 = datetime.datetime.now()
    if (message['check'] != ""):
        emit('my_response',
             {'question': message['data'], 'username': message['check'], 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': results_text, 'count': session['receive_count']})
        # recordMysql.record_create(message['check'], message['data'], results_text, time1, time2)
    else:
        warning = '亲，只有登录后才可以查询课表哦！'
        emit('my_response',
             {'question': message['data'], 'username': message['check'], 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': warning, 'count': session['receive_count']})


# 登录监听函数
@socketio.on('my_login_event', namespace='/test')
def get_login_message(message):
    username, password = message["username"], message['password']
    return_password = informationMysql.information_query(username)

    if(len(return_password)==0):
        emit("login_backtips_event", {'data': '该账号未注册！'})
        return 0
    else:
        if(message['password'] == return_password):
            print("python 登录成功");
            emit("login_success_event",{'data' : '登录成功'})
            get_record_message(message["username"])  #调用函数返回聊天记录
            return 1#[1,message["username"]]
        else:
            emit("login_backtips_event", {'data': '密码错误！'})
            return 0#[0,False]

# 得到登陆用户的聊天记录
def get_record_message(username):
    db = pymysql.connect(host='localhost', user='root', database='user_information', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM record WHERE USERID='%s'" % (username)   #后期数据库表中可能会改列名，到时候换一下。
    try:
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录元组
        print(results)
    except:
        print("Error: unable to fetch data")
    db.close()
    if(len(results)>=3):
        emit("add_histiry_event", {'username': username, 'one1': results[-3][2], "one1_re": results[-3][3],
                               'two': results[-2][2], "two_re": results[-2][3],
                               'three': results[-1][2], "three_re": results[-1][3],
                               "one_time": results[-3][4].strftime('%Y-%m-%d %H:%M:%S'),
                               "one_re_time": results[-3][5].strftime('%Y-%m-%d %H:%M:%S'),
                               "two_time": results[-2][4].strftime('%Y-%m-%d %H:%M:%S'),
                               "two_re_time": results[-2][5].strftime('%Y-%m-%d %H:%M:%S'),
                               "three_time": results[-1][4].strftime('%Y-%m-%d %H:%M:%S'),
                               "three_re_time": results[-1][5].strftime('%Y-%m-%d %H:%M:%S')})

        return results[-1],results[-2],results[-3]  #所有的聊天记录
    #如果聊天用户只与机器人聊了两组对话，那么将只会显示两组对话
    elif(len(results)==2):
        emit("add_histiry_event1", {'username': username, 'one1': results[0][2], "one1_re": results[0][3],
                                   'two': results[1][2], "two_re": results[1][3],
                                   "one_time": results[0][4].strftime('%Y-%m-%d %H:%M:%S'),
                                   "one_re_time": results[0][5].strftime('%Y-%m-%d %H:%M:%S'),
                                   "two_time": results[1][4].strftime('%Y-%m-%d %H:%M:%S'),
                                   "two_re_time": results[1][5].strftime('%Y-%m-%d %H:%M:%S')
                                    })
        return results[-1], results[-2] # 所有的聊天记录
    # 如果聊天用户只与机器人聊了一组对话，那么将只会显示一组对话
    elif(len(results)==1):
        emit("add_histiry_event2", {'username': username, 'one1': results[0][2], "one1_re": results[0][3],
                                    "one_time": results[0][4].strftime('%Y-%m-%d %H:%M:%S'),
                                    "one_re_time": results[0][5].strftime('%Y-%m-%d %H:%M:%S')
                                    })
        print(results[0][2],results[0][3],results[0][4].strftime('%Y-%m-%d %H:%M:%S'),results[0][5].strftime('%Y-%m-%d %H:%M:%S'))
        return results[-1]


# 左侧点击事件查询课表
@socketio.on('get_push_message', namespace='/test')
def push_table_message(message):
    grades, classes, directions, days, check = message["text1"], message['text2'], message['text3'], message['text4'], message['check']

    if(grades == "2017级"):
        messages = grades + directions + days
    else:
        messages = grades + classes + days

    # 计算现在是第几周的代码
    today = datetime.date.today()
    date1 = time.strptime('2019-09-02', "%Y-%m-%d")
    date2 = time.strptime(str(today), "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    days_number = (date2 - date1).days
    # 得到这周是多少周
    this_week = math.ceil(days_number / 7)
    print(type(this_week))

    # 这是2017级查询
    if re.search('\w+方向', messages):
        if re.search('\d\d\d\d级', messages) and re.search('星期\D{1}', messages):
            grade = re.findall('\d\d\d\d级', messages)
            #class1 = re.findall('\d-\d班', messages)
            day = re.findall('星期\D', messages)
            direction = re.findall('[H,J,软，人]\w+方向', messages)
            results_text = scheduleMysql.class_schedule_query1(grade[0],str(this_week), day[0],direction[0])

    # #这是2018和2019级查询
    elif re.search('\d\d\d\d级', messages) and re.search('[1-8]班', messages) and re.search('星期\D{1}',messages):
        grade = re.findall('\d\d\d\d级', messages)
        class1 = re.findall('[1-8]班', messages)
        day = re.findall('星期\D', messages)
        results_text = scheduleMysql.class_schedule_query(grade[0], class1[0], str(this_week), day[0])

    session['receive_count'] = session.get('receive_count', 0) + 1
    time1 = datetime.datetime.now()

    if(check!=''):
        emit("push_table_event",{'data': results_text, 'time': time1.strftime('%Y-%m-%d %H:%M:%S')})
    else:
        warning = '亲，只有登录后才可以查询课表哦！'
        emit('push_table_event',{'data': warning, 'time': time1.strftime('%Y-%m-%d %H:%M:%S')})

# 注册监听函数
@socketio.on('my_register_event', namespace='/test')
def get_register_message(message):
    print(informationMysql.information_query(message["username"]))
    if (len(message["username"]) == 0):
        print('用户名不能为空！')
        emit("register_tips_event", {'data': '用户名不能为空！'})
    elif (len(message["studentid"]) != 10):
        print('学号不合法！')
        emit("register_tips_event", {'data': '学号不合法！'})
    elif(informationMysql.information_query_sid(message["studentid"])):
        print('该学号已被注册')
        emit("register_tips_event", {'data': '该学号已被注册'})
    elif (len(message["email"]) == 0):
        print('邮箱不能为空！')
        emit("register_tips_event", {'data': '邮箱不能为空！'})
    elif(len(message["password"])==0):
        print('密码长度不能为空！')
        emit("register_tips_event", {'data': '密码长度不能为空！'})
    elif(message["password"]!= message["lastpass"]):
        print('两次密码不一致！')
        emit("register_tips_event", {'data': '两次密码不一致！'})
    else:
        username, studentid, email, password = message['username'], message['studentid'], message['email'], message[
            'password']
        x = informationMysql.information_create(studentid, username, email, password)
        emit("register_success_event", {'data': '注册成功'})

from PIL import Image
# 图片转换
@socketio.on('tran_img_event', namespace='/test')
def tran_img_event(message):
    print("tran_img_event")
    img = base64.b64decode(message["data"])
    file = open('1.jpg', "wb")
    file.write(img)
    file.close()
    img = Image.open('1.jpg')
    output = img.resize((150, 30), Image.ANTIALIAS)
    print(np.shape(output))
    output.save('1.jpg')
    # img = Image.open(BytesIO(img))
    # img.thumbnail((100, 100))  # 图片压缩
    #out = com.main('1.jpg')
    out = zyq.main()
    time1 = datetime.datetime.now()
    time2 = datetime.datetime.now()
    str2 = ''
    out = str2.join(out)
    if (message['check'] != ""):
        emit('my_response',
             {'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': out})
        print(message['data'])
        recordMysql.record_create1(message['check'], message['data'], out, time1, time2,1)
    else:
        emit('my_response',
             {'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': out})


# 手写汉字识别


@socketio.on('hand_write_event', namespace='/test')
def tran_img_event(message):
    img = base64.b64decode(message["data"])
    file = open('2.png', "wb")
    file.write(img)
    file.close()

    out = hw.predict_test()
    time1 = datetime.datetime.now()
    time2 = datetime.datetime.now()
    str2 = ''
    out = str2.join(out)
    if (message['check'] != ""):
        emit('my_response',
             {'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': out},
             broadcast=True)
        print(message['data'])
        recordMysql.record_create1(message['check'], message['data'], out, time1, time2,1)
    else:
        emit('my_response',
             {'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': out},
             broadcast=True)


@socketio.on('map_event', namespace='/test')
def tran_img_event(message):
    print(message["data"])
    flag = map.baidu_map(message["data"])
    time1 = datetime.datetime.now()
    time2 = datetime.datetime.now()
    if(flag==0):
        emit('my_response',
             {'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': '输入地址不合法，请尝试重新输入！'},
             )
    else:
        emit('my_response2')
if __name__ == '__main__':
    socketio.run(app, debug=True,use_reloader=False)
