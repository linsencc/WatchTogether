import functools

from flask import render_template, make_response, request
from flask_login import login_required, current_user
from flask_socketio import emit, disconnect

from app import app, socketio, socketio_namespace
from sync import Room, User, Manage


manage = Manage()


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            app.logger.info('authenticated fail')
            disconnect()
        else:
            app.logger.info('%s authenticated success' % current_user.nickname)
            return f(*args, **kwargs)
    return wrapped


@socketio.on('connect', namespace=socketio_namespace)
@authenticated_only
def connected_msg():
    if current_user.is_authenticated:
        nickname = current_user.nickname
        app.logger.info('%s connected...' % nickname)
    else:
        app.logger.info('authenticated fail')


@socketio.on('disconnect', namespace=socketio_namespace)
@authenticated_only
def disconnect_msg():
    nickname = current_user.nickname
    app.logger.info('%s disconnected...' % nickname)


@socketio.on('my_event', namespace=socketio_namespace)
def mtest_message(message):
    app.logger.info(message)
    emit('respond', {'data': message['data'], 'count': 'server respond'})



@app.route('/join', methods=['GET', 'POST'])
def index():
    # return make_response("Watch together")
    return render_template('socketio/index.html')


@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    print(current_user.nickname, ' in test')
    return make_response({'data': {'a': 1, 'b': 2, 'c': 3}})


@app.route('/join-room', methods=['POST'])
@login_required
def join_room():
    post_data = request.get_json()
    room_number = str(post_data.get('room-number', None))

    user = User(current_user.email, current_user.nickname)
    room = manage.get_room(room_number)

    msg = '%s already in room(%s)' % (current_user.nickname, room_number)
    code = 1

    if current_user.email not in room.users:
        room.add_user(user)
        msg = '%s join room(%s)' % (current_user.nickname, room_number)
        code = 0

    users_info = room.get_users_info()
    app.logger.info(msg)
    return make_response({'code': code, 'msg': msg, 'data': {'room_number': room_number, 'room': users_info}})


@app.route('/leave-room', methods=['POST'])
@login_required
def leave_room():
    post_data = request.get_json()
    room_number = str(post_data.get('room-number', None))

    room = manage.get_room(room_number)
    msg = '%s not in room(%s)' % (current_user.nickname, room_number)
    code = 1

    if current_user.email in room.users:
        room.delete_user(current_user.email)
        msg = '%s leave room(%s)' % (current_user.nickname, room_number)
        code = 0

    users_info = room.get_users_info()
    app.logger.info(msg)
    return make_response({'code': code, 'msg': msg, 'data': {'room_number': room_number, 'room': users_info}})


