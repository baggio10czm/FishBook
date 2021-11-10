"""
 User: Czm
 Date: 2021/11/1
 Time: 13:32
"""
from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


# 引入其他model对象最好放在引用处,避免对象重复引用报错
# from app.models.wish import Wish


class Gift(Base):
    """
    relationship关联User,ForeignKey设置关联的id
    """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    # 是否赠送出去了
    launched = Column(Boolean, default=False)
    # unique=True这里不需要,因为要赠送的书不是唯一存在的,多个用户可能都会送同一本书
    isbn = Column(String(15), nullable=False)

    # 本项目book是通过api方式获得,就不用关联book数据表了
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('user.id'))

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        """ 根据用户id查询他所有要赠送的礼物(倒序) """
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_count(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn,到Wish表中查询出某个礼物的Wish心愿数量
        # query(需要查询的字段或信息)
        # filter_by 是调用filter = 更强大灵活,可传入条件表达式
        # func.count 得到数量        # mysql in 查询
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == 0,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
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

    # 对象代表一个礼物,具体的个体
    # 类代表礼物这个事物,它是抽象的,不是一个具体的事物
    @classmethod
    def recent(cls):
        """
        首页:最新要赠送的礼物
        :return:
        """
        # limit 放最后面
        # distinct 去重,必须结合 group_by 分组使用
        # desc 倒序
        recent_gifts = cls.query.filter_by(launched=False).group_by(
            cls.isbn).order_by(
            desc(cls.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gifts
