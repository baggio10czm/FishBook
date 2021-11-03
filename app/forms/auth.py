"""
 User: Czm
 Date: 2021/11/1
 Time: 14:30
"""
from wtforms import StringField, PasswordField, Form
from wtforms.validators import length, DataRequired, ValidationError, Email, EqualTo

# 从 WTForms 2.3.0 版本开始，电子邮件验证由名为email-validator的外部库处理。
# 如果要启用电子邮件验证支持，则需要安装带有额外要求的 WTForms email
from app.models.user import User

"""
$ pip install wtforms[email]
或者你可以email-validator直接安装：

$ pip install email-validator
或者你可以回到旧版本的 WTForms：

$ pip install wtforms==2.2.1
"""


class RegisterForm(Form):
    # 字符串验证 8-64位
    email = StringField(validators=[DataRequired(), length(8, 64),
                                    Email(message='输入邮箱不正确')])
    # 密码
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入密码'), length(
            6, 32, message='6-32位密码')])

    nickname = StringField(validators=[
        DataRequired(), length(2, 10, message='昵称至少需要两个字符,最多10个字符')
    ])

    @staticmethod
    def validate_email(field):
        # filter_by 参数可以有多个
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已被注册!')

    @staticmethod
    def validate_nickname(field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称被注册!')


class LoginForm(Form):
    # 字符串验证 8-64位
    email = StringField(validators=[DataRequired(), length(8, 64),
                                    Email(message='输入邮箱不正确')])
    # 密码
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入密码'), length(
            6, 32, message='6-32位密码')])


class ForgetPasswordForm(Form):
    # 字符串验证 8-64位
    email = StringField(validators=[DataRequired(), length(8, 64),
                                    Email(message='输入邮箱不正确')])


class ResetPasswordForm(Form):
    # 密码
    password1 = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入密码'),
        length(6, 32, message='6-32位密码'),
        EqualTo('password2', message='两次输入密码不相同')
    ])
    password2 = PasswordField(validators=[
        DataRequired(),
        length(6, 32, message='6-32位密码')
    ])
