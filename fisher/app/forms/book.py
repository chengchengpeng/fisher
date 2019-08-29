# wtforms是需要下载的包
# StringField校验文本，IntegerFiled校验数字，然后使用关键字validators，validators接受一组参数，用Length约束文本长度
#            用NumberRange约束数字大小
# 实例化该对象的的时候接受一组参数，来源于其继承的Form父类的构造函数
# DataRequired()验证器能够使空格不通过验证

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


class SearchForm(Form):
    # q = StringField(validators=[NumberRange(min=1, max=99)], default=1)
    # page = IntegerField(validators=[DataRequired(), Length(min=1, max=30)], default=1)

    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)

class DriftForm(Form):
    recipient_name = StringField(vaildators=[DataRequired(), Length(min=2, max=20,
                                             message='收件人是的姓名长度必须在2到20个字符之间')])
    message = StringField()
    mobile = StringField(validators=[DataRequired(),Length(min=10, max=70,
                                                           message='地址符不到10个字吗？尽量写详细些吧')])