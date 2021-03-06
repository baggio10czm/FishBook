"""
 User: Czm
 Date: 2021/11/3
 Time: 16:48
"""
from app.libs.enums import PendingStatus


class DriftCollection:
    def __init__(self, drifts, current_user_id):
        # 这样不用像book列出那么多属性
        # 但这样会导致类的属性看起来不是一目了然
        # 结合gift drift book 一般是推荐用book的方式写对象
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}
        # 这里不直接调用current_user里的id 增加解耦性
        self.data = self.__parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        """
        判断用户是否是请求者
        :param drift:
        :param current_user_id:
        :return:
        """
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_id):
        you_are = self.requester_or_gifter(drift, current_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'drift_id': drift.id,
            'you_are': you_are,
            # 'book_title': drift.gift.book.title,
            # 'book_author': drift.gift.book.author_str,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status_str': pending_status,
            'status': drift.pending
        }
        return r
