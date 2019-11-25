#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, redirect,\
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    print(message)

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': '您说的"' + message['data'] + '"我已经收到了', 'count': session['receive_count']},
         broadcast=True)


# {'data': message['data'], 'count': session['receive_count']},

if __name__ == '__main__':
    socketio.run(app, debug=True)
