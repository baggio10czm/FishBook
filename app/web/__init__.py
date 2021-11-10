# 蓝图
from flask import Blueprint, render_template

web = Blueprint('web', __name__)


# 拦截所有404报错,跳转自己定义的404页面
@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# app的init文件 导入(from app.web.book import web)
# __init__ 自动导入以下模块
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
