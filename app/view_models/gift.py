"""
 User: Czm
 Date: 2021/11/2
 Time: 14:58
"""
from .book import BookViewModel
# 做为rest api 不利于序列化 就不用namedtuple了
# from collections import namedtuple

# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        """
        尽量不要修改实例属性,可能不利于理解整体的代码(不知道哪里更改了)
        :return:
        """
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    # 避免嵌套 遍历创建一个方法
    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
            r = {
                'id': gift.id,
                'wishes_count': count,
                'book': BookViewModel(gift.book)
            }
            return r
        # gift.book 是原始数据需要用BookViewModel实例化处理
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
