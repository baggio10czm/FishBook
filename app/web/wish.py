from flask import current_app, flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import web

__author__ = '七月'

from app.models.base import db
from app.models.wish import Wish
# from ..view_models.wish import MyWishes
from ..libs.email import send_mail
from ..models.gift import Gift
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
            # flask_login 的 current_user 是用户对于的user模型
            # 前后端分离项目,用户信息是保存在token中
            gift.uid = current_user.id
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单,请不要重复添加!')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    """
        向他人赠送此书
        向想要这本书的人发送一封邮件
        注意，这个接口需要做一定的频率限制
        这接口比较适合写成一个ajax接口
    """
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有增加此书到赠送清单,添加前请确保自己可赠送此书!')
    else:
        send_mail(wish.user.email, '有人想送你一本书', 'email/satisify_wish.html',
                  wish=wish, gift=gift)
        flash('已向他/她发送了一封邮件,如果赠送成功,你将受到一个鱼漂!')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    """
    # 撤销心愿清单
    :param isbn:
    :return:
    """
    wish = Wish.query.filter_by(uid=current_user.id, isbn=isbn).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
