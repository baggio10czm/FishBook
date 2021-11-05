"""
 User: Czm
 Date: 2021/11/3
 Time: 12:05
"""
from app.libs.enums import PendingStatus
from app.models.base import Base
from sqlalchemy import Column, Integer, String, SmallInteger


class Drift(Base):
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(200), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息(不关联其他表,保留历史信息,优化查询性能)
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    # 状态,因为基类中有status了所以用pending
    # 不能与下面的同名所以改成 _pending
    _pending = Column('pending', SmallInteger, default=1)

    # 改写pending获取时是获得对应的枚举
    @property
    def pending(self):
        return PendingStatus(self._pending)

    # 改写pending设置时是设置的枚举对应的值
    @pending.setter
    def pending(self, status):
        self._pending = status.value

    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester_id = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')
