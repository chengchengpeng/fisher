# 验证密码用PasswordField类型
# 当参数验证失败后，所有的错误信息，都是在form.errors里的。也能在form里拿到填写的错误数据。
""" 对于需要业务性质的参数的校验，则要自定义验证器,验证器函数名用validate_开头，下划线后面接要验证的变量名
函数中传入参数名为field,该参数有wtforms自动传入，field.data可以拿到field的值，函数内需要raise.ValidationError()函数抛出异常，如果函数执行到这一步，表明
验证不通过
"""
# 数据库查询可以用模型名.query.filter_by().first(),filter()函数内可以传入一组查询条件，first（）表示取查询结果的第一条
# EqualTo可以用来判断输入的新密码和旧密码是不是相等
from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                      Email(message='电子邮箱不符合规范')])

    password = PasswordField(validaors=[
        DataRequired(message='密码不能为空请输入正确密码'), Length(6,32)])

    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='昵称至少为两个字符，最为十个字符')
    ])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已经被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经存在')

class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(validator=[
        DataRequired(message='密码不尅为空，请输入你密码'), Length(6,32)
    ])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validator=[
        DataRequired(),
        Length(6, 12, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('passwords', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)])