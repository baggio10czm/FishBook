"""
 User: Czm
 Date: 2021/10/29
 Time: 14:03
"""
from app.models.base import Base


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']
        self.isbn = book['isbn']
        self.binding = book['binding']
        self.pubdate = book['pubdate']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return "/".join(list(intros))


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


# 老的面向过程的写法
class _BookViewModel:
    # 描述特征(类变量/实例变量)
    # 行为(方法)
    # 以下代码面向过程
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @staticmethod
    def __cut_book_data(data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            # 空值处理
            'pages': data['pages'] or '',
            'price': data['price'],
            'author': '、'.join(data['author']),
            # 空值处理
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book
