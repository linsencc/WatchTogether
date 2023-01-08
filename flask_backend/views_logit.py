import functools

from flask import render_template, make_response, request
from flask_login import login_required, current_user
from flask_socketio import emit, disconnect

from app import app, socketio, socketio_namespace
from sync import Room, User, Manage


manage = Manage()


@app.route('/test-socket', methods=['GET', 'POST'])
def index():
    return render_template('socketio/index.html')


@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    print(current_user.nickname, ' in test')
    return make_response({'data': {'a': 1, 'b': 2, 'c': 3}})


@app.route('/create-room', methods=['POST'])
@login_required
def create_room():
    post_data = request.get_json()
    room_number = str(post_data.get('roomNumber', None))

    if room_number == '' or room_number == 'None':
        msg = 'room number(%s) cannot be empty' % room_number
        app.logger.info(msg)
        return make_response({'code': 1, 'msg': msg, 'data': {}})

    if room_number in manage.rooms:
        msg = 'room(%s) already exists' % room_number
        app.logger.info(msg)
        return make_response({'code': 1, 'msg': msg, 'data': {}})

    room = manage.create_room(room_number)
    user = User(current_user.email, current_user.nickname)
    room.add_user(user)

    msg = 'room(%s) create success' % room_number
    app.logger.info(msg)
    users_info = room.get_users_info()
    return make_response({'code': 0, 'msg': msg, 'data': {'room_number': room_number, 'room': users_info}})


@app.route('/join-room', methods=['POST'])
@login_required
def join_room():
    post_data = request.get_json()
    room_number = str(post_data.get('roomNumber', None))

    if room_number not in manage.rooms:
        msg = 'room(%s) does not exist' % room_number
        app.logger.info(msg)
        return make_response({'code': 1, 'msg': msg, 'data': {}})

    # room = manage.get_room(room_number)

    # todo get room 这部分的代码需要提前
    # if current_user.email in manage.user_to_room:
    #     msg = '%s already in room(%s)' % (current_user.nickname, room_number)
    #     app.logger.info(msg)
    #     return make_response({'code': 1, 'msg': msg, 'data': {}})

    user = User(current_user.email, current_user.nickname)
    room.add_user(user)
    users_info = room.get_users_info()

    msg = '%s join room(%s)' % (user.nickname, room_number)
    app.logger.info(msg)
    return make_response({'code': 0, 'msg': msg, 'data': {'room_number': room_number, 'room': users_info}})


@app.route('/leave-room', methods=['POST'])
@login_required
def leave_room():
    post_data = request.get_json()
    room_number = str(post_data.get('roomNumber', None))

    if room_number not in manage.rooms:
        msg = 'room(%s) does not exist' % room_number
        app.logger.info(msg)
        return make_response({'code': 1, 'msg': msg, 'data': {}})

    room = manage.get_room(room_number)

    if current_user.email not in room.users:
        msg = '%s not in room(%s)' % (current_user.email, room_number)
        app.logger.info(msg)
        return make_response({'code': 1, 'msg': msg, 'data': {}})

    room.delete_user(current_user.email)

    users_info = room.get_users_info()
    msg = '%s leave room(%s)' % (current_user.nickname, room_number)
    app.logger.info(msg)
    return make_response({'code': 0, 'msg': msg, 'data': {'room_number': room_number, 'room': users_info}})


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            app.logger.info('socket authenticated fail')
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('connect', namespace=socketio_namespace)
@authenticated_only
def connected_msg():
    nickname = current_user.nickname
    app.logger.info('%s socket connected...' % nickname)


@socketio.on('disconnect', namespace=socketio_namespace)
@authenticated_only
def disconnect_msg():
    nickname = current_user.nickname
    app.logger.info('%s socket disconnected...' % nickname)


@socketio.on('user-init', namespace=socketio_namespace)
@authenticated_only
def mtest_message(message):

    app.logger.info(message)
