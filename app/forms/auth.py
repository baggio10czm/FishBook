"""
 User: Czm
 Date: 2021/11/1
 Time: 14:30
"""
from wtforms import StringField, PasswordField, Form
from wtforms.validators import Length, DataRequired, ValidationError, Email, EqualTo

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


class EmailForm(Form):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
                                            Email(message='电子邮箱不符合规范')])


class LoginForm(EmailForm):
    # 密码
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入密码'), Length(
            6, 32, message='6-32位密码')])


class ResetPasswordForm(Form):
    # 密码
    password1 = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入密码'),
        Length(6, 32, message='6-32位密码'),
        EqualTo('password2', message='两次输入密码不相同')
    ])
    password2 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='6-32位密码')
    ])


class RegisterForm(EmailForm):
    # 密码
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入密码'), Length(
            6, 32, message='6-32位密码')])

    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符,最多10个字符')
    ])

    def validate_email(self, field):
        # filter_by 参数可以有多个
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已被注册!')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称被注册!')
