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


tuling='3d3fa6b66f72479eaa9c45be57b639e0'
api_url = "http://openapi.tuling123.com/openapi/api/v2"


@socketio.on('my_broadcast_event', namespace='/test')
def get_message(message):
    time1=datetime.now()
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

    if "怎么做" in message['data']:
        results_text = response_dic['results'][0]['values']['url']
    else:
        results_text = response_dic['results'][0]['values']['text']

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data':  results_text, 'count': session['receive_count']},
         broadcast=True)
    time2=datetime.now()
    # judge=get_login_message(message)
    # if judge>0:
    if (message['check']!=""):
        recordMysql.record_create(message['userId'], message['data'], results_text, time1, time2)
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
            return 1
        else:
            emit("login_backtips_event", {'data': '密码错误！'})
            return 0
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

if __name__ == '__main__':
    socketio.run(app, debug=True)
