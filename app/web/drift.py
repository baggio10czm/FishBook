from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from . import web


from app.models.base import db

from ..forms.book import DriftForm
from ..libs.email import send_mail
from ..libs.enums import PendingStatus
from ..models.drift import Drift
from ..models.gift import Gift
from app.view_models.drift import DriftCollection
from ..models.user import User
from ..models.wish import Wish


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书你老人家自己就有!那索取个啥?')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        # 可以考虑 email/短信 通知
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                  wisher=current_user, gift=current_gift)
    giver = current_gift.user.summary
    return render_template('drift.html', gifter=giver, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    # 用filter可以实现复杂查询,or_改成'或'关系
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
        拒绝请求，只有书籍赠送者才能拒绝请求
        注意需要验证超权
    """
    with db.auto_commit():
        # 用filter 因为查询了两个表(Gift,Drift)
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """
        撤销所要书籍
        防止超权 + requester_id=current_user.id
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    """
        已邮寄对方索要的书籍
    """
    with db.auto_commit():
        # 用filter 因为查询了两个表(Gift,Drift)
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success

        # 赠送完成
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

        # 心愿完成
        Wish.query.filter_by(uid=drift.requester_id,
                             isbn=drift.isbn, launched=False).update({Wish.launched: True})
        return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        # drift...
        # 用populate_obj一次搞定以上过程
        # 模型和form中的字段名要求一致
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = current_gift.book

        drift.book_title = book['title']
        drift.book_author = book['author']
        drift.book_img = book['image']
        drift.isbn = book['isbn']
        # 扣除一个鱼豆,可以加一个判断是否为负数(报错)
        current_user.beans -= 1

        db.session.add(drift)
