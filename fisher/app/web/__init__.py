# @web.qpp_errorhandler(404)用下在遇到相应的异常就执行，被装饰的视图函数，函数内可以做各种操作
from flask import Blueprint, render_template

web = Blueprint('web', __name__)


@web.qpp_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
# 如果不导入下面这些模块，他们将不会执行


from app.web import book
# from app.web import user
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
