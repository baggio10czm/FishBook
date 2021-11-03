from app import create_app

app = create_app()

if __name__ == '__main__':
    # threaded=True 开启多线程
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81, threaded=True)

