from flask import Flask, make_response

app = Flask(__name__)
# 配置文件
app.config.from_object('config')
print(app.config['DEBUG'])


@app.route('/html')
def html():
    # 自己写 response
    headers = {
        'content-type': 'text/plain',
        # 'location': 'http://www.guilinenguang.org'
    }
    response = make_response('<html>Hello Czm!</html>', 200)
    response.headers = headers
    # response.set_cookie()
    # 返回 response 对象的方式
    # return response
    # 最简单的方式
    # return "<h3>hello Czm!</h3>"
    # 常用的方法
    return '<html>hello Czm!</html>', 200, headers

# 注册路由另一种方式
# app.add_url_rule('/html', view_func=html)


# host='0.0.0.0' 支持本地ip访问,
# debug=True 开启调试模式支持不需要重启就更新代码
# if __name__ == '__main__'  防止在生产环境nginx+uwsgi服务器上,启动flask服务器
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=80)
