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
#
# # app 应用配置
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 关闭对模型修改的监控
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
#
#
# # 数据库设置
# db = SQLAlchemy(app)
#
#
# # # websocket设置
# socketio = SocketIO(app)
# socketio.init_app(app, cors_allowed_origins='*')
#
#
# # 用户登录插件设置
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
#
#
# # 加载views中逻辑函数，models中数据模型，不可删除
# from flask_backend import views
# from flask_backend import auth
# from flask_backend import socketio_view
#
