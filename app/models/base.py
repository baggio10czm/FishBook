"""
 User: Czm
 Date: 2021/11/1
 Time: 13:36
"""
from contextlib import contextmanager
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import SmallInteger, Column, Integer


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=None):
        """
            contextmanager 装饰器可将类改变成上下文管理器
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            # %r 用来做 debug 比较好，因为它会显示变量的原始数据
            current_app.logger.exception('%r' % e)
            if throw:
                raise e


class Query(BaseQuery):
    """
    重写基类的方法,避免每个filter_by都需要传 status=1
    但这样的写法确实不太懂...
    """
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


# query_class 重写覆盖
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 模型基类 不需要生成数据表 __abstract__
    __abstract__ = True
    # 不能再类变量设置具体的值,不然所有实例变量都是一样的值
    create_time = Column('create_time', Integer)
    # 支持软删除
    status = Column(SmallInteger, default=1)

    def __init__(self):
        # 存入当前时间的时间戳
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            # 判断对象是否包含某个属性
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            # 时间戳转换成时间对象,后续就可以用 strftime('%Y-%m-%d') 转成日期
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    # 软删除,使代码更加语义化
    def delete(self):
        self.status = 0
