import functools
from flask_backend.app import socketio, app
from flask_socketio import emit, disconnect
from flask_login import current_user


namespace_room = '/dcenter'


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


@socketio.on('connect', namespace=namespace_room)
@authenticated_only
def connected_msg():
    if current_user.is_authenticated:
        nickname = current_user.nickname
        app.logger.info('%s connected...' % nickname)
    else:
        app.logger.info('authenticated fail')


@socketio.on('disconnect', namespace=namespace_room)
@authenticated_only
def disconnect_msg():
    nickname = current_user.nickname
    app.logger.info('%s disconnected...' % nickname)


@socketio.on('my_event', namespace=namespace_room)
def mtest_message(message):
    app.logger.info(message)
    emit('respond', {'data': message['data'], 'count': 'server respond'})
