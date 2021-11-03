from flask import current_app, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import web

__author__ = '七月'

from app.models.base import db
from app.models.wish import Wish
# from ..view_models.wish import MyWishes
from ..view_models.trade import MyTrade


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_count(isbn_list)
    view_model = MyTrade(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Wish()
            gift.isbn = isbn
            gift.uid = current_user.id
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单,请不要重复添加!')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
