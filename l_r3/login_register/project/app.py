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

# import project.user_information_mysql as informationMysql
# import project.user_record_mysql as recordMysql
from datetime import datetime
import pymysql
import datetime
import base64
#import matplotlib.pyplot as plt
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


# @socketio.on('my_broadcast_event', namespace='/test')
# def test_broadcast_message(message):
#     print(message)
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': '您说的"' + message['data'] + '"我已经收到了', 'count': session['receive_count']},
#          broadcast=True)


# {'data': message['data'], 'count': session['receive_count']},


#tuling='3d3fa6b66f72479eaa9c45be57b639e0'  #老师的
tuling='e238e5b6de7545fc886720c0d175cb79'    #自己的
# b9c94835bf924281b681248828c006d1
api_url = "http://openapi.tuling123.com/openapi/api/v2"

flag = ''
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
        "apiKey": 'b9c94835bf924281b681248828c006d1',
        #"apiKey": '3d3fa6b66f72479eaa9c45be57b639e0',
        "userId": message['userId']
    }
    }
    req = json.dumps(req).encode('utf8')
    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    response_dic = json.loads(response_str)

    # if "怎么做" in message['data']:
    #     results_text = response_dic['results'][0]['values']
    #     #results_text = response_dic['intent']['code']
    # elif "图片" in message['data']:
    #     results_text = response_dic['results'][0]['values']['image']
    # else:

    print(response_dic)
    results_text = response_dic['results'][0]['values']['text']

    #print("怎么做：" + results_text)

    session['receive_count'] = session.get('receive_count', 0) + 1
    time2 = datetime.datetime.now()


    # judge=get_login_message(message)
    # if judge>0:
    if(message['check']!=""):
        emit('my_response',
             {'question': message['data'], 'username': message['check'], 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': results_text, 'count': session['receive_count']},
             broadcast=True)
        recordMysql.record_create(message['check'], message['data'], results_text, time1, time2)
    else:
        emit('my_response',
             {'question': message['data'], 'username': '匿名用户', 'time1': time1.strftime('%Y-%m-%d %H:%M:%S'),
              'time2': time2.strftime('%Y-%m-%d %H:%M:%S'), 'data': results_text, 'count': session['receive_count']},
             broadcast=True)


#login
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


#得到登陆用户的聊天记录
def get_record_message(username):
    db = pymysql.connect(host='localhost', user='root', database='user_information', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM record WHERE USERID='%s'" % (username)   #后期数据库表中可能会改列名，到时候换一下。
    try:
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录元组
        # print(results)
    except:
        print("Error: unable to fetch data")
    db.close()
    print(results[-1], results[-2], results[-3])
    print(results[-2][2],results[-3][2])
    emit("add_histiry_event", {'username': username, 'one1': results[-3][2], "one1_re": results[-3][3],
                               'two': results[-2][2], "two_re": results[-2][3],
                               'three': results[-1][2], "three_re": results[-1][3],
                               "one_time": results[-3][4].strftime('%Y-%m-%d %H:%M:%S'),
                               "one_re_time": results[-3][5].strftime('%Y-%m-%d %H:%M:%S'),
                               "two_time": results[-2][4].strftime('%Y-%m-%d %H:%M:%S'),
                               "two_re_time": results[-2][5].strftime('%Y-%m-%d %H:%M:%S'),
                               "three_time": results[-1][4].strftime('%Y-%m-%d %H:%M:%S'),
                               "three_re_time": results[-1][5].strftime('%Y-%m-%d %H:%M:%S')})

    print(results[-1][4].strftime('%Y-%m-%d %H:%M:%S'),results[-2][4].strftime('%Y-%m-%d %H:%M:%S'),results[-3][4].strftime('%Y-%m-%d %H:%M:%S'))
    print(results[-1][5].strftime('%Y-%m-%d %H:%M:%S'), results[-2][5].strftime('%Y-%m-%d %H:%M:%S'), results[-3][5].strftime('%Y-%m-%d %H:%M:%S'))
    return results[-1],results[-2],results[-3]  #所有的聊天记录

#register
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
##图片转换
@socketio.on('tran_img_event', namespace='/test')
def tran_img_event(message):
    img = base64.b64decode(message["data"])


if __name__ == '__main__':
    socketio.run(app, debug=True,use_reloader=False)
