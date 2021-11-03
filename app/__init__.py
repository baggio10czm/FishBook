from flask import Flask
from flask_login import LoginManager
from app.models.base import db
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    # 配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    register_blueprint(app)
    # 注册db
    db.init_app(app)
    # 注册flask_login
    login_manager.init_app(app)
    # 给login_manager制定登录页面
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册!'

    # 注册mail
    mail.init_app(app)

    # 加这个解决"Missing user_loader or request_loader"报错.不知道为什么
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return None

    # 用 with是第一种解决"Working outside of application context."报错的方法
    # 详细解释在test.py
    with app.app_context():
        db.create_all()
    # 这是第二种解决办法
    # db.create_all(app=app)
    # 第三种解决办法 是在model db = SQLAlchemy()里传入app(根据项目情况选择)

    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
