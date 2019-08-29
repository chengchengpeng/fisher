# 所有用view_model处理数据都应该放在视图函数中
from flask import render_template

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from . import web


@web.route('/')
def index():
    books= [BookViewModel(gift.book) for gift in Gift.recent()]
    return render_template('index.html', recent=books)