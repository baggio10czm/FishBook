from flask import current_app, flash, redirect, url_for, render_template

from . import web
# login_required 装饰器验证是否登录
from flask_login import login_required, current_user
__author__ = '七月'

from app.models.gift import Gift
from app.models.base import db
from app.models.user import User
# from ..view_models.gift import MyGifts
from ..libs.enums import PendingStatus
from ..models.drift import Drift
from ..view_models.trade import MyTrade


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_count(isbn_list)
    view_model = MyTrade(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # try:
        # 改成 with 高级语法
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
            # db.session.commit()
        # except Exception as e:
        #     # 最好在所有db.session.commit()的地方+ try……except
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单,请不要重复添加!')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    """
    # 撤销赠送清单
    :param isbn:
    :return:
    """
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    hasDrift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.Waiting).first()
    if hasDrift:
        flash('此礼物已经在漂流中,请去<鱼漂>操作撤销,才能此操作!')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))


