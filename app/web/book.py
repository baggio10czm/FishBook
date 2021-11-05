"""
重复导入会导致路由注册失效
用蓝图解决分文件的问题
from FishBook import app
"""
# import json

from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from . import web

# @web.route('/book/search/<q>/<page>')
from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import _BookViewModel, BookCollection, BookViewModel
from app.view_models.trade import TradeInfo


@web.route('/test1')
def test1():
    from flask import request
    from app.test.LocalStackThread import n
    print(n.v)
    n.v = 99
    print('~~~~~~~~~~~~~~~`')
    # request 进程隔离特性保证它的值不被影响(污染)
    # 而引入一个普通对象(n),它的值就很容易被污染
    print(getattr(request, 'v', None))
    setattr(request, 'v', 99)
    print('-------------')
    return ''


@web.route('/test')
def test2():
    data = {
        'name': 'czm',
        'age': 36,
        'do': 'things',
        'nothing': '',
    }
    flash('hello wwW', category='error')
    flash('hello CZM', category='warning')
    # 模板渲染
    # return render_template('layout.html', data=data)
    return render_template('test.html', data=data)


books = BookCollection()


@web.route('/book/search')
def search():
    # request 必须是视图函数中才有用
    # request.args 默认是不可变的字典,使用 .to_dict()改变为正常字典
    # q = request.args['q']
    # page = request.args['page']
    form = SearchForm(request.args)
    # 验证通过
    if form.validate():
        # 去掉空白
        q = form.q.data.strip()
        # 使用 form里面的参数值比较好,在没有传page时可变为默认值1
        page = form.page.data
        # 先判断参数是书名还是isbn
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # result = YuShuBook.search_by_isbn(q)
            # result = _BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q, page)
            # result = YuShuBook.search_by_keyword(q, page)
            # result = _BookViewModel.package_collection(result, q)
        # 用flask,jsonify格式化
        books.fill(yushu_book, q)
        # 用lambda 处理所有需要处理的对象
        # return json.dumps(books, default=lambda o: o.__dict__)
        # jsonify 无法处理对象
        # return jsonify(books.__dict__)
    else:
        flash('搜索的关键字不符合要求,请<重装系统>^_^')
    return render_template('search_result.html', books=books)
    # 用自带的比较麻烦
    # return json.dumps(result), 200, {'content-type': 'application/json'}


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 先判断用户是否登录,因为用户不可能同时在赠送和心愿表
    # 所以加一个else 可能可以减少一次查询
    if current_user.is_authenticated:
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True
        else:
            if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                    launched=False).first():
                has_in_gifts = True

    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           )
