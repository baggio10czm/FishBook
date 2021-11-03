"""
 User: Czm
 Date: 2021/11/3
 Time: 12:05
"""
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
    pending = Column('pending', SmallInteger, default=1)

    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester_id = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')
