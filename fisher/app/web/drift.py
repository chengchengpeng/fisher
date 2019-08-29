""" 当一个类的内部实现了__call__方法，就可以和调用方法一样来调用，叫做可调用对象,直接调用对象就是调用__call__方法，
在类里面方法很少，或者某个方法使用的次数特别多的时候，可以将这个类写成一个课调用对象，另外最主要的是统一了调用接口
"""
# first_or_404，当数据库查询不到数据是，就抛出一个异常404
#  drift_form.populate_obj()可将form对象下的所有字段拷贝到模型中，传入参数为模型名，，但属性名要相同
# 对于查询条件是or关系的查询，用filter来查询，见查询条件当做参数插入_or()然后查询
# filter查询两个表，filter查询一个表
# 如果要更改数据库中的某个属性，查询出来然后update(),传入的参数为字典，模型属性为键，要修改的值为值
# 调用函数可以先被调用然后定义
from operator import or_

from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.dift import DriftCollection
from app.web import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_youself_gift(current_user.id):
        flash ('这本书是你自己的，不能向你自己所要')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enought_beans.htm;', beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_mail(current_user.email,'有人想要一本书', 'email/get_gift',
                  wisher=current_user,
                  gift=current_gift)
        return redirect(url_for('web.pending'))

        gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beas)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(desc(Drift.create_time)).all
    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)

@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id,
                                   Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))

@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    # 超权
    # uid :1  did:1
    # uid :2  did:2
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))

@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += 1
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True

#  A  Wish
#  A  Drift
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))

def save_drift(drift_form, current_gift):
    drift = Drift()
    with db.auto_commit():
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.nickname
        drift.requester_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id
        book = BookViewModel(current_gift.book.first)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1