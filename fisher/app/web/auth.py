# request.form 提供post提交过来的表单信息
# request.args.get获得？后面的相关查询参数
# request.method可以拿到服务端传来的是POST或者GET
# 要在数据库里新增一条数据，首先要实例化这个模型
# 为数据模型赋值，自己直接用obj.key = value    模型.属性 = 值
# 网页跳转可以用redirect()函数，即重定向
"""要使用插件需要引入函数login_user，将user模块传入函数中，可以传入一个关键字参数remember = True,来实现记住密码的功能，使用这个函数，我们需要将一个代表性的属性做标记
用于写入cooking，即在User模块下...详细见User模块
"""
# request.args.get('next')可以获取?后面next的url
# url_for()接受一个视图函数为参数，用于生成这个指向这个视图函数的url
# 字符串.startswith(符号)，用于判断字符串是否用符号开头
# 登录插件，提供了一个变量current_user，可以拿到用户发id，current_user实际是实例化里一个用户模型，current_user简介操作了cooking
# 要使用事物，来保证数据的一致性，并且要使用回滚，如果不使用回滚，当前数据插入出现了错误，以后数据插入还是发生错误
# login_user()就是将cooking清理掉
from flask import request, render_template, redirect, url_for, flash

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from . import web
from flask_login import login_user
from app.libs.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    # request.form
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validata():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)

        return redirect(url_for('web.login'))
    return render_template('auth/reaister.html', form={'data': {}})

@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或者密码错误')
    return render_template('auth/login.html', form=form)

@web.route('/logout')
def login():
    login_user()
    return redirect(url_for(web.index))


@web.route('/reset/password', method=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.quer.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data, '重置你的密码',
                      'email/reset_password_.html', user=user,
                      token=user.generate_token())
            flash('一封电子邮件已发送到邮箱' + account_email + '请及时查收')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', method=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)
