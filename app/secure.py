"""
 User: Czm
 Date: 2021/10/28
 Time: 22:30
"""

# 重要的配置信息,可不上传git
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:111222@localhost:3306/fisher'
# ‘SQLALCHEMY_TRACK_MODIFICATIONS’ 这项配置在未来的版本中会被默认为禁止状态，
# 把它设置为True即可取消warning。
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'asgeq215xzvdyhDEWTDSHFGK548346VBMGF4'

# user_login cookie保存时间 值为天数,默认是365天
# REMEMBER_COOKIE_DURATION = 15


# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '122300413@qq.com'
MAIL_PASSWORD = 'jtgmsoukiwhebgia'
MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '鱼书<hello@yushu.im>'

