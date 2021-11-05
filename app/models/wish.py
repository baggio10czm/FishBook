"""
 User: Czm
 Date: 2021/11/1
 Time: 17:40
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db
# 引入其他model对象最好放在引用处,避免对象重复引用报错
# from app.models.gift import Gift
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    """
    relationship关联User,ForeignKey设置关联的id
    """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)
    # unique=True这里不需要,因为要赠送的书不是唯一存在的,多个用户可能都会送同一本书
    isbn = Column(String(15), nullable=False)

    # 本项目book是通过api方式获得,就不用关联book数据表了
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('user.id'))

    @classmethod
    def get_user_wishes(cls, uid):
        """
        根据用户id查询他所有要赠送的礼物
        :param uid:
        :return:
        """
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_count(cls, isbn_list):
        from app.models.gift import Gift
        # 根据传入的一组isbn,到Gift表中查询出某个礼物的Gift数量
        # filter_by 是调用filter 更强大灵活,可传入条件表达式
        # func.count
        # mysql in 查询
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{'count': count[0], 'isbn': count[1]} for count in count_list]
        return count_list

    @property
    def book(self):
        """
        根据礼物的isbn得到书籍的详细信息
        :return:
        """
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

