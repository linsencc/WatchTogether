import functools
from flask_backend.app import socketio, app
from flask_socketio import emit, disconnect
from flask_login import current_user


namespace_room = '/dcenter'


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('connect', namespace=namespace_room)
@authenticated_only
def connected_msg():
    nickname = current_user.nickname
    print('%s connected...' % nickname)


@socketio.on('disconnect', namespace=namespace_room)
@authenticated_only
def disconnect_msg():
    nickname = current_user.nickname
    print('%s connected...' % nickname)


@socketio.on('my_event', namespace=namespace_room)
def mtest_message(message):
    print(message)
    emit('xxxx', {'data': message['data'], 'count': 1})
