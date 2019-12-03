#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, redirect,\
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import json
import urllib.request
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
    results_text = response_dic['results'][0]['values']['text']
    print(results_text)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data':  results_text, 'count': session['receive_count']},
         broadcast=True)

#login
@socketio.on('my_login_event', namespace='/test')
def get_login_message(message):
    print(message["username"])
    print(message['password'])
    data_base = ["123"]
    if(len(data_base)==0):
        emit("login_backtips_event", {'data': '该账号未注册！'})
    else:
        if(message['password'] == data_base[0]):
            print("python 登录成功");
            emit("login_success_event",{'data' : '登录成功'})
        else:
            emit("login_backtips_event", {'data': '密码错误！'})

#register
@socketio.on('my_register_event', namespace='/test')
def get_register_message(message):
    print(message["username"])
    print(message["studentid"])
    print(message["email"])
    print(message["password"])
    print("python 注册成功")
    emit("register_success_event", {'data': '注册成功'})



if __name__ == '__main__':
    socketio.run(app, debug=True)
