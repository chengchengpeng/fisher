# jsonify是flask提供的
# ?传参时：request.args能够获取用户的各种请求信息，并且是一个不可变的字典，可以通过to_dick()方法变成可变字典
# Form类下的validator()为真时表示验证通过，反正验证失败
# strip()方法可以消除字符串前后空格
# json.dump() 可以传入一个函数，，实现了代码解释权的反转，让函数的调用方，来描述函数的功能。
# 对象的内置方法，__dict__可以用来打印对象的属性
# 单页面通过js来访问API然后加载数据是在服务器进行的，有称之为AJAX技术
# 判断用户是否登录可以用current_user下面的一个属性is_authenticated

from flask import jsonify, request, render_template, flash

import json

from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YushuBook

# 蓝图
# app.config_object('config) 可以读取配置文件中的所有参数


@web.route('/test')
def test():
    r = {
        'name': '七月',
        'age': '18'
    }
    r1 = {

    }
    flash('hello,qiyue',category='error')
    return render_template('test1.html', data=r, data1=r1)


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data

        # q = request.args['q']
        # page = request.args['page']
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YushuBook()
        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)

            # result = YuShuBook.search_by_isbn(q)
            # result = BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q.page)

            # result = YuShuBook.search_by_isbn(q, page)
            # result = BookViewModel.package_collection(result, q)
        books.fill(yushu_book, q)
        # return json.dump(books, delattr(lambda o: o.__dict__))

        # return jsonify(books)
    else:
        flash('搜索关键字不符合要求，请重新输入')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu_book = YushuBook()
    yushu_book.search_by_isbn(isbn)
    book =BookViewModel(yushu_book.first)
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = False

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model,
                           gifts=trade_gifts_model, has_in_wishs=has_in_wishes,
                           has_in_gifts=has_in_gifts)
