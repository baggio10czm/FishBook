"""
 User: Czm
 Date: 2021/11/1
 Time: 13:36
"""
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import SmallInteger, Column, Integer


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            # 最好在所有db.session.commit()的地方+ try……except
            self.session.rollback()
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
    create_time = Column('create_time', Integer)
    # 支持软删除
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            # 判断对象是否包含某个属性
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    # 软删除,使代码更加语义化
    def delete(self):
        self.status = 0
