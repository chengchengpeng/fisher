# 需要改变模型属性名在数据库中的字段名，只需要在Column()里传递一个字符串
# @property用来读取属性定义一个同名的函数，并打上装饰器@password.setter，用来写入数据
# 如果要实现类的一个属性可读不可写，就用@property,@password.setter。第二个装饰器的函数不赋值，返回异常，不可写
# werkzeug.security里面有个函数generate_password_hash可以用来加密
# check_password_hash可以用来的比对加密后的密码和原始密码，传入两个参数，第一个参数为加密后的密码，第二个为传入的要比对的密码
""" 要标记写入cooking的属性，需要第一一些特定的函数，这些函数在UserMixin类里已经写好了只需要将User模型继承该类，，其中
最重要的方法为get_id(),该方法默认写入cooking的值为id，如果要改变，需要定义一个get_id方法来返回一个新的值
"""
"""使用@login_required装饰器来区分视图函数的权限，还需要写一个函数,get_user(uid)，要想插件识别该函数，需要在函数上打装饰器
@login_manager.user_loader,当去数据库中数据的条件为主键时，没必要用filter_by,用get就够了，login_manager需要导入
"""
# TimedJSONWebSignatureSerializer用来加密，可以将其理解为一个序列化器，第一个参数传入一段随机字符串,dumps()像序列化器中写入数据，接受参数为字典
# decode('utf-8')将字节码转换成字符串
# 数据库查询的触发语句用count()就可以直接得到查询出来的数量
from math import floor

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YushuBook

from sqlalchemy import Column, Integer, String, Boolean, Float


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(64), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # 读
    @property
    def password(self):
        return self._password

    # 写
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YushuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        gifting = Gift.quer.filter_by(uid=self.id, isbn=isbn,
                                      launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

        def generate_token(self, expiration=600):
            s = Serializer(current_app.config['SECRET_KEY'], expiration)
            return s.dumps({'id': self.id}).decode('utf-8')


        @staticmethod
        def reset_password(token,new_password):
            s = Serializer(current_app.cofig['SECRET_KEY'])
            # 反向去序列化器中的数据
            try:
                data = s.loads(token.encode('utf-8'))
            except:
                return False
            uid = data.get('id')
            with db.auto_commit():
                user = User.quer.get(uid)
                user.password = new_password
            return True

        def can_send_drift(self):
            if self.beans < 1:
                return False
            success_gifts_count = Gift.query.filter_by(
                uid = self.uid, launched=True).count()
            success_receive_count = Drift.query.filter_by(
                requester_id=self.id, pending=PendingStatus.Success).count()

            return True if \
                floor(success_receive_count / 2) <= floor(success_gifts_count) \
                else False

        @property
        def summary(self):
            return dict(
                nickname=self.nickname,
                beans=self.beans,
                email=self.email,
                send_receive=str(self.seng_counter) + '/' + str(self.receive_counter)
            )

# def get_id(self):
#     return self.id
# 把id号转换成了用户模型
@login_manager.user_loader
def get_use(uid):
    return User.query.get(int(uid))
