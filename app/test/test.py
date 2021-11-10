"""
 User: Czm
 Date: 2021/10/28
 Time: 22:36
"""
from flask import Flask, current_app

app = Flask(__name__)
# 应用上下文 对象 Flask
# 请求上下文 对象 Request
# Flask AppContext
# Request RequestContext
# 离线应用/单元测试需要手动推入上下文(因为不是从浏览器发起请求)
# 因为这没有发起请求,所以app的栈是空的
# 所以就会出现"Working outside of application context."的错误
# 需要手动入栈避免错误,push()入  pop()出
# ctx = app.app_context()
# ctx.push()
# a = current_app
# d = a.config['DEBUG']
# print(d)
# ctx.pop()

# 简化写法
# with app.app_context():
#     a = current_app
#     d = a.config['DEBUG']

# 实现了上下文协议的对象使用with
# 上下文管理器 带有 __enter__(push)  __exit__ (pop) 方法
# 上下文表达式必须要返回一个上下文管理器
# app_context return  AppContext()
# with

# 文件读写
# try:
#     f = open(r'D:\t.txt')
#     print(f.read())
# finally:
#    f.close()


# with open(r'') as f:
#     print(f.read())


class MyResource:
    def __enter__(self):
        print('connect to resource')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_tb 不是空时就说明出错了
        if exc_tb:
            print('process exception')
        else:
            print('no exception')
        print('close resource connection')
        # 返回True 等于没有异常需要处理, 返回False(或不返回) 等于有异常需要外部处理
        return True

    def query(self):
        print('query data')


# as obj_A 是 __enter__ 返回的值
try:
    with MyResource() as resource:
        resource.query()
except Exception as ex:
    raise ex
