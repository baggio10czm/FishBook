"""
 User: Czm
 Date: 2021/11/2
 Time: 21:04
"""
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            # 可以写入日志或其他处理
            raise e


def send_mail(to, subject, template, **kwargs):
    # 参数依次:标题、发送邮件者、正文body(可传一些简单文本，本项目用模板就不需设置body了)、发送目标（支持群发）
    msg = Message(f'<鱼书>{subject}',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 因为通过第三方发送邮件比较慢，前台页面会处理加载状态
    # 用户体验不好，所以开启新线程处理发送邮件，异步处理。
    # 但如果只传msg过去会报错“Working outside of application context.”
    # 解决缺少上下文的问题，传入current_app是不行的，因为开启新线程以后
    # current_app 所指向的是新线程中的 app（它不存在）所以必须
    # 把真实不会变的flask 实例化传过去
    # 对性能要求不高,尽量不要异步编程(并发)
    app = current_app._get_current_object()
    threading = Thread(target=send_async_email, args=[app, msg])
    threading.start()
