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
from project import class_schedule_mysql as scheduleMysql
from project import zyq
from datetime import datetime
import pymysql
import datetime
import re

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
#tuling='e238e5b6de7545fc886720c0d175cb79'    #自己的
api_url = "http://openapi.tuling123.com/openapi/api/v2"


@socketio.on('my_broadcast_event', namespace='/test')
def get_message(message):
    time1=datetime.datetime.now()
    print(message)
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
                "city": "深圳",
                "province": "广州",
                "street": "XXX"
            }
        }
    },
    "userInfo":
    {
        "apiKey": '3d3fa6b66f72479eaa9c45be57b639e0',
        "userId": message['userId']
    }
    }
    req = json.dumps(req).encode('utf8')
    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)

    #计算现在是第几周的代码
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
    if re.search('\w+方向',message['data']):
        if re.search('\d\d\d\d级',message['data'])and re.search('\d-\d班',message['data']) and re.search('星期\D{1}',message['data']):
            grade = re.findall('\d\d\d\d级', message['data'])
            class1 = re.findall('\d-\d班', message['data'])
            day = re.findall('星期\D', message['data'])
            direction = re.findall('\w+方向', message['data'])
            # print(grade, class1, day, direction, str(this_week))
            # print(grade[0], class1[0], str(this_week), day[0],direction[0])
            results_text = scheduleMysql.class_schedule_query1(grade[0], class1[0], str(this_week), day[0],direction[0])
            # print('我是调用的第二个函数')
    #询问某道菜怎么做时，直接返回url
    elif "怎么做" in message['data']:
        results_text = response_dic['results'][0]['values']['url']
    # #这是2018和2019级查询
    elif re.search('\d\d\d\d级',message['data']) and re.search('[1-8]班',message['data']) and re.search('星期\D{1}',message['data']):
        grade = re.findall('\d\d\d\d级', message['data'])
        class1 = re.findall('[1-8]班', message['data'])
        #week = re.findall('\d{1,2}周', message['data'])
        day = re.findall('星期\D', message['data'])
        #print(type(scheduleMysql.class_schedule_query(grade[0],class1[0],week[0],day[0])))
        results_text=scheduleMysql.class_schedule_query(grade[0],class1[0],str(this_week),day[0])
        # print('我是第一个函数')
    else:
        results_text = response_dic['results'][0]['values']['text']

    # print("怎么做："+results_text)
    session['receive_count'] = session.get('receive_count', 0) + 1
    time2 = datetime.datetime.now()



    # judge=get_login_message(message)
    # if judge>0:
    if(message['check']!=""):
        emit('my_response',
             {'question': message['data'], 'username': message['check'], 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': results_text, 'count': session['receive_count']}
             )
        recordMysql.record_create1(message['check'], message['data'], results_text, time1, time2,0)
    else:
        emit('my_response',
             {'question': message['data'], 'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': results_text, 'count': session['receive_count']}
             )


# 登录监听函数
@socketio.on('my_login_event', namespace='/test')
def get_login_message(message):
    username, password = message["username"], message['password']
    #print(type(password))
    return_password = informationMysql.information_query(username)
    #print(type(return_password))
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
    results = recordMysql.record_query(username)
    if(len(results)==0):
        return 0
    find_index=[]
    upward=-1
    while(len(find_index)<3 and upward>-1*len(results)):
        if(results[upward][6]!='1'):
            find_index.append(upward)
        upward-=1
    while(len(find_index)<3 and len(find_index)>0):
        find_index.append(find_index[0])

    if (len(find_index) > 0):
        emit("add_histiry_event", {'username': username, 'one1': results[find_index[2]][2], "one1_re": results[find_index[2]][3],
                                   'two': results[find_index[1]][2], "two_re": results[find_index[1]][3],
                                   'three': results[find_index[0]][2], "three_re": results[find_index[0]][3],
                                   "one_time": results[find_index[2]][4].strftime('%Y-%m-%d %H:%M:%S'),
                                   "one_re_time": results[find_index[2]][5].strftime('%Y-%m-%d %H:%M:%S'),
                                   "two_time": results[find_index[1]][4].strftime('%Y-%m-%d %H:%M:%S'),
                                   "two_re_time": results[find_index[1]][5].strftime('%Y-%m-%d %H:%M:%S'),
                                   "three_time": results[find_index[0]][4].strftime('%Y-%m-%d %H:%M:%S'),
                                   "three_re_time": results[find_index[0]][5].strftime('%Y-%m-%d %H:%M:%S'),
                                   "one_flag": results[find_index[2]][6],
                                   "two_flag": results[find_index[1]][6],
                                   "three_flag": results[find_index[0]][6]})

    return 0

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
        # if x > 0:
        #     emit("register_success_event", {'data': '注册成功'})
        print('注册成功')
        emit("register_success_event", {'data': '注册成功'})

# 图片转换
@socketio.on('tran_img_event', namespace='/test')
def tran_img_event(message):
    img = base64.b64decode(message["data"])
    file = open('1.jpg', "wb")
    file.write(img)
    file.close()
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
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': out},
             broadcast=True)
        print(message['data'])
        recordMysql.record_create1(message['check'], message['data'], out, time1, time2,1)
    else:
        emit('my_response',
             {'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': out},
             broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True,use_reloader=False)
