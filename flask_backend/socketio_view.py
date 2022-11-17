from flask_backend.app import socketio, app


namespace_room = '/room'


@socketio.on('connect', namespace=namespace_room)
def connected_msg():
    print('client connected...')


@socketio.on('disconnect', namespace=namespace_room)
def disconnect_msg():
    print('client disconnected...')


@socketio.on('my_event', namespace=namespace_room)
def my_event():
    print('my_event')


@app.route('/push')
def push_once():
    event_name = 'room'
    data = {'data': "test message!"}
    sockent_rsp = socketio.emit(event_name, data, broadcast=False, namespace=namespace_room)
    print(sockent_rsp)
    return 'done!'
