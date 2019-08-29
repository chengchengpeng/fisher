# 并不是实例化了一个核心对象就能使用这个核心对象，需要去一个叫栈的地方去，而且用完之后会推出去；
# register_blue app的方法，用来将蓝图插入app
# app.config.from_object()可以用来载入配置文件
# db.init_app(app)方法可以将db和app关联起来
# db.create_all()来创建数据库表
# __name__决定了app是这个项目的根目录
# flask提供了一个将数据写入cooking的插件，首先要初始化这个插件，login_manager.init_app(app)将这个插件和app相关联
"""写入cooking是为了实现一些功能，有些函数需要登录才能访问，只有携带cooking的用户才能访问,插件,flask_login提供了一
个装饰器，@login_required，只要在一个视图函数上打上了这个装饰器，就要登录才能访问，要使用该插件，还需要为插件编写一个函数，见user模块
"""
""" 可以用login_manager.login_view = url使在访问需要登录的页面的时候跳转到url指向的页面，此时会闪现一条错误信息，
可以用login_manager.login_message= '请先登录或者注册'来自定义错误信息， 在跳转页面的url里不止有该页面的url，还有一个next参数，该参数就是原网页url
"""
# 所有的插件都都要在这个模块下注册，首先引用插件的模块，然后实例化，最后使用init_app()把app传进去
from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail
from app.models.book import db

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__ , static_folder=)

    # 用提取app中的配置参数

    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message= '请先登录或者注册'

    mail.init_app(app)
    #
    # with app.app_context():
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)