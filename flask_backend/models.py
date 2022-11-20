from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_backend.app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    nickname = db.Column(db.String(64))         # 用户名
    password_hash = db.Column(db.String(128))   # 密码散列值

    def set_password(self, password):           # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):      # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

