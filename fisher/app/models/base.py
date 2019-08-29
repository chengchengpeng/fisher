# 当一个模型只是作为一个基类，而不用在数据库中建表是，可以使用__abstract__ = True来表明
# hasattr()接受两个参数，第一个是对象，第二个参数为key,该函数为判断函数是否包含参数为key的属性
# setattr()接受三个参数，第一个为要赋值的对象，第二是为对象的哪一个属性key赋值,第三个是赋什么值value

# 将数据写入数据库中，首先要实例化数据库模型，然后对个模型属性赋值，调用db.session.add(模型)方法和db.session.commit()方法即可，这是ORM的数据库操作思想
# 只要使用到了db.session,commit()就使用try:   except Exception as e : db.session.rollback()
# 给一个函数打上了装饰器contextmanager,就可以将该函数用with来使用 见test/context模块
# 取当前时间用datetime.now()，用timestamp将时间改为时间搓
# 类变量是所有对象共享的变量在，在类创建的时候就确定了，
# create_time是一个整数，先使用datetime.fromtimestamp()方法将其转换为时间格式

# super 用于调用父类的方法
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger
from datetime import datetime


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(Query)


class Base(db.Model):
    # 使这个表不被创建
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 充分利用python动态语言的特性
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.item():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
