# import os
# import sys
#
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from flask_socketio import SocketIO
#
#
# # 如果是 Windows 系统，使用三个斜线
# WIN = sys.platform.startswith('win')
# prefix = 'sqlite:///' if WIN else 'sqlite:////'
#
# # app 应用配置
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 关闭对模型修改的监控
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
#
# # 数据库设置
# db = SQLAlchemy(app)
#
# # # websocket设置
# socketio = SocketIO(app)
# socketio.init_app(app, cors_allowed_origins='*')
#
# # 用户登录插件设置
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
#
# # 加载views中逻辑函数，models中数据模型，不可删除
# from flask_backend import views
# from flask_backend import auth
# from flask_backend import socketio_view



# from flask_backend import app, socketio
# from geventwebsocket.handler import WebSocketHandler
# from gevent.pywsgi import WSGIServer
#
#
# import logging
# logging.basicConfig(level=logging.DEBUG)
#
#
# if __name__ == '__main__':
#     http_server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
#     http_server.serve_forever()





from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

name_space = '/dcenter'


@app.route('/')
def index():
    return render_template('socketio/index.html')

@app.route('/push')
def push_once():
    event_name = 'dcenter'
    broadcasted_data = {'data': "test message!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return 'done!'

@socketio.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')


@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    print('client disconnected.')


@socketio.on('my_event', namespace=name_space)
def mtest_message(message):
    print(message)
    emit('my_response',
         {'data': message['data'], 'count': 1})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
