from datetime import timedelta

from flask import Flask, request, jsonify, session
from flask_cors import CORS  # 导入CORS库

app = Flask(__name__)
# app.secret_key 修改的时候会造成失效
app.config['SECRET_KEY'] = 'lihongjun'
# 设置过期时间，类型是timedelta，写数字不报错、但是不生效，注意！！！
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
# 配置全局路由
CORS(app, supports_credentials=True)


# @app.route('/api/querySession', methods=['POST'])
# # def querySession():
# #     getJson = request.get_json()
# #     sessionExist = getJson["bagCap"]
# #     res = {
# #         "sessionExist": 0,
# #
# #     }
# #     return jsonify(res)

# 设置session测试
@app.route('/test/testSession', methods=['GET'])
def setSession():
    session['userPhone'] = '18031589519'
    return 'success'


@app.route('/api/querySession', methods=['GET'])
def querySession():
    userPhone = session.get('userPhone')
    print(userPhone)
    if userPhone is None:
        sessionExit = 0
    else:
        sessionExit = 1  
    res = {
        "sessionExist": sessionExit,
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run()
