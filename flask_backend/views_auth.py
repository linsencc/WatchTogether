import json
import time

from flask import request, make_response, render_template
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, login_manager
from models import User


# 用户加载回调函数
@login_manager.user_loader
def load_user(email: str):                # 创建用户加载回调函数，接受用户 Email 作为参数
    user = User.query.get(str(email))     # 用 Email 作为 User 模型的主键查询对应的用户
    return user


# 用户注册
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        post_data = request.get_json()
        account = post_data.get('account', None)
        password = post_data.get('password', None)
        nickname = post_data.get('nickname', None)

        # 账号或密码为空
        if not account or not password or not nickname:
            rsp = {'code': 1, 'msg': '账号密码和昵称不能为空', 'data': {}}
            return make_response(rsp, 400)

        # 检查用户是否被注册
        user = User.query.filter_by(email=account).first()
        if user:
            rsp = {'code': 1, 'msg': '账号已被注册', 'data': {}}
            return make_response(rsp, 400)

        # 用户注册
        user = User()
        user.email = account
        user.nickname = nickname
        user.set_password(password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)

        rsp = {'code': 0, 'msg': '注册成功', 'data': {}}
        return make_response(rsp, 200)

    if request.method == 'GET':
        return render_template("template/auth/login.html")

    # 兜底回复
    rsp = {'code': 1, 'msg': '注册失败', 'data': {}}
    return make_response(rsp, 400)


# 用户登录
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        post_data = request.get_json()
        account = post_data.get('account', None)
        password = post_data.get('password', None)

        # 账号或密码为空
        if not account or not password:
            rsp = {'code': 1, 'msg': '账号和密码不能为空', 'data': {}}
            return make_response(rsp, 400)

        # 从数据库获取对应用户
        user = User.query.filter_by(email=account).first()

        # 验证用户名和密码是否一致
        if user and user.validate_password(password):
            login_user(user, remember=True)
            rsp = {'code': 0, 'msg': '登录成功', 'data': {'nickname': user.nickname, 'email': user.email}}
            app.logger.info(rsp)
            return make_response(rsp, 200)

        rsp = {'code': 1, 'msg': '登录验证失败', 'data': {}}
        return make_response(rsp, 400)

    if request.method == 'GET':
        return render_template("auth/login.html")

        # 兜底回复
    rsp = {'code': 1, 'msg': '登录失败', 'data': {}}
    return make_response(rsp, 400)


# 用户登出
@app.route('/sign-out', methods=['GET', 'POST'])
@login_required
def sign_out():
    try:
        user_email = current_user.email
        logout_user()
        rsp = {'code': 0, 'msg': user_email + ' logout'}
        return make_response(rsp)
    except Exception as e:
        rsp = {'code': 1, 'msg': str(e)}
        return make_response(rsp)


# 用户信息
@app.route('/profile', methods=['GET', 'POST'])
def get_profile():
    resp_data = {'code': 1, 'data': {}}

    if current_user.is_authenticated:
        resp_data['code'] = 0
        resp_data['data'] = current_user.to_dict(rules=('-password_hash', '-id'))

    app.logger.info(resp_data)
    return make_response(resp_data)
