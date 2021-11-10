"""
 User: Czm
 Date: 2021/11/1
 Time: 13:36
"""
from math import floor

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


# 继承UserMixin 可以不用初始化flask_login的很多方法
# 如果表的主键 命名不是id 就需要重写覆盖 get_id 方法
class User(UserMixin, Base):
    # __tablename__ 改变表的名字默认是类的名字
    # __tablename__ = 'user1'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    _password = Column('password', String(228), nullable=False)

    @property
    def password(self):
        """
        读取密码
        :return:
        """
        return self._password

    @password.setter
    def password(self, raw):
        """
        写入密码,这两方法可以对属性预处理
        :return:
        """
        self._password = generate_password_hash(raw)

    def can_send_drift(self):
        # 索取者鱼豆必须大于1
        if self.beans < 1:
            return False
        # 索取者每索取两本必须先送出一本
        # 成功送出去的书的数量
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        # 成功收到书的数量
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        # 首先判断 isbn是否符合格式规范
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        # 然后验证这个isbn是否是存在
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的图书
        # 一个用户不可能同时成为赠送者和索要者
        # 既不在自己赠送清单中(还没被送出),也不在心愿清单才可添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    # flask_login 设置保存的id
    # def get_id(self):
    #     return self.id

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # 生成包含用户id的加密字符,+decode是把byte变成字符串
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return False
        uid = data.get('id')
        with db.auto_commit():
            # 这里可以加入user判断用户是否存在或是有效
            user = User.query.get(uid)
            user.password = new_password
        return True

    @property
    def summary(self):
        """ 用户简历 """
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


# 设置login_manager
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
