from flask import request, make_response
from flask_login import login_user, login_required, logout_user, current_user

from flask_backend.app import app, db
from flask_backend.app import login_manager
from flask_backend.models import User


# 用户加载回调函数
@login_manager.user_loader
def load_user(email: str):                # 创建用户加载回调函数，接受用户 Email 作为参数
    user = User.query.get(str(email))     # 用 Email 作为 User 模型的主键查询对应的用户
    return user


# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        post_data = request.get_json()
        account = post_data.get('account', None)
        password = post_data.get('password', None)
        nickname = post_data.get('nickname', None)

        # 账号或密码为空
        if not account or not password or not nickname:
            rsp = {'code': 1, 'msg': '账号、密码和昵称不能为空', 'data': {}}
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

        rsp = {'code': 0, 'msg': '注册成功', 'data': {}}
        return make_response(rsp, 200)

    # 兜底回复
    rsp = {'code': 1, 'msg': '注册失败', 'data': {}}
    return make_response(rsp, 400)


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        post_data = request.get_json()
        account = post_data.get('account', None)
        password = post_data.get('password', None)

        # 账号或密码为空
        if not account or not password:
            rsp = {'code': 1, 'msg': '账号与密码不能为空', 'data': {}}
            return make_response(rsp, 400)

        # 从数据库获取对应用户
        user = User.query.filter_by(email=account).first()

        # 验证用户名和密码是否一致
        if user and user.validate_password(password):
            login_user(user)
            rsp = {'code': 0, 'msg': '登录成功', 'data': {}}
            return make_response(rsp, 200)

        rsp = {'code': 1, 'msg': '登录验证失败', 'data': {}}
        return make_response(rsp, 400)

    if request.method == 'GET':
        rsp = {'code': 0, 'msg': 'use post for login', 'data': {}}
        return make_response(rsp, 200)

    # 兜底回复
    rsp = {'code': 1, 'msg': '登录失败', 'data': {}}
    return make_response(rsp, 400)


# 用户登出
@app.route('/logout', methods=['GET', 'POST'])
@login_required             # 用于视图保护
def logout():
    try:
        user_email = current_user.email
        logout_user()
        rsp = {'code': 0, 'msg': user_email + ' logout'}
        return make_response(rsp)
    except Exception as e:
        rsp = {'code': 1, 'msg': str(e)}
        return make_response(rsp)
