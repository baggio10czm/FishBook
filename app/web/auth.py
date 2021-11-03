from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from . import web
from flask_login import login_user, logout_user
from app.models.base import db

__author__ = '七月'

from app.models.user import User


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            # 写入模型
            user = User()
            user.set_attrs(form.data)
            # 写入数据库
            db.session.add(user)
            # db.session.commit()
            # 一定要加return 结束视图函数执行
            return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # remember 保存状态 默认值是365天,可以在配置文件中更改
            login_user(user, remember=True)
            # 获得url上的参数
            next_url = request.args.get('next')
            # not next_url.startswith('/') 如果不是以'/'开头的
            # 手动在url上输出其他网站的url,防止重定向攻击
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            # 一定要加return 结束视图函数执行
            return redirect(next_url)
        else:
            flash('账户不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = ForgetPasswordForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            # __call__ 把对象变成可调用对象
            # first_or_404 的作用是停止代码运行并抛出异常，简化代码
            # 在web.__init__ 里设置了对404的拦截,显示自己定义的404页面
            user = User.query.filter_by(email=account_email).first_or_404()
            # if not user:
            #     raise Exception()
            from app.libs.email import send_mail
            send_mail(form.email.data, '重置您的密码',
                      'email/reset_password.html', user=user,
                      token=user.generate_token())
            flash(f'一封邮件已发送到邮箱{account_email}，请及时查收。')
            # return redirect(url_for('web.login'))
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('您的密码已更新，请使用新密码登录！')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败,有效设置时间可能已经过期')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))

