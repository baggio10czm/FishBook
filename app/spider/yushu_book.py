# 不能按照教程用hLengthtp命名,不知道是不是和某包有冲突?
from app.libs.httper import HTTP
from flask import current_app


class YuShuBook:
    # 描述特征(类变量/实例变量)
    # 行为(方法)
    # 以下代码面向过程
    # isbn_url = 'https://api.douban.com/v2/book/isbn/{}'
    # keyword_url = 'https://api.douban.com/v2/book/search?apikey=0df993c66c0c636e29ecbb5344252a4a&q={}&count={}&start={}'
    keyword_url = 'http://t.talelin.com/v2/book/search?q={}&count={}&start={}'
    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.__calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    @staticmethod
    def __calculate_start(page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        """
        更合理的api设计,返回调用方想要的、方便使用的数据
        直接返回一本书的详情,不需要 xxx.books[0]
        """
        return self.books[0] if self.total > 0 else None
