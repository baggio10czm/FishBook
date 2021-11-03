"""
 User: Czm
 Date: 2021/11/1
 Time: 22:35
"""
from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(good) for good in goods]

    @staticmethod
    def __map_to_trade(single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = "不确定"
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrade:
    """
    把wish和gift同样的逻辑合并为一套代码就可以了，wish和gift不需要了
    可以把把MyTrade作为wish和gift的基类
    如果他们的逻辑改变了，就可以继承MyTrade，在做其他逻辑的处理
    在合并之中会报“ 'None' has no attribute 'book'”的错误
    合并之后就没有了，不知道为什么……
    """
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list
        self.trades = self.__parse()

    def __parse(self):
        """
        尽量不要修改实例属性,可能不利于理解整体的代码(不知道哪里更改了)
        :return:
        """
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    # 避免嵌套 遍历创建一个方法
    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'id': trade.id,
            'wishes_count': count,
            'book': BookViewModel(trade.book)
        }
        return r
        # gift.book 是原始数据需要用BookViewModel实例化处理
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
