# 项目入口文件
import uuid

from flask import Flask, jsonify, request

# 解决浏览器同源策略导致的跨域问题
from flask_cors import CORS

# 解决string SQL 由warning 变成了 Coercion的问题
from sqlalchemy.sql import text

# 导入数据库实例
from database import db

# 导入数据库配置
from config import *

from spyder.spyderSouhu import *

# 引入定时器，用来定时对网站进行爬取，以二十四小时为时间
from flask_apscheduler import APScheduler
import time

class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 添加API

scheduler = APScheduler()

# 实例化flask
app = Flask(__name__)

# 配置转码，支持中文，防止乱码
app.config["JSON_AS_ASCII"] = False

# 配置mysql数据库
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{}:{}@{}:{}/{}".format(
    mysqlUser, mysqlPassword, mysqlHost, mysqlPort, mysqlDb)

# 自动提交sql请求
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True

db.init_app(app)

# 配置跨域
CORS(app, cors_allowed_origins="*")


# 注意一个问题，采用restful风格的接口的话，用的方法比较多，而对应的request获取参数的方法也是不同的
# 现代编程很少有一个功能一个接口这种形式了，而是采用类视图来进行封装，因此下面这种接口我全部注释掉
# 删除接口
# @app.route("/delete/", methods=["DELETE"])
# def deleteApi():
#     userId = request.args.get("id", None)
#
#     # 下划线主要是提示自己这个东西不能被改变，是写死的内容
#     _sql = "delete from `user` where `id` = {}".format(userId)
#
#     print(_sql)
#
#     db.session.execute(text(_sql))
#
#     return jsonify({"errcode": 0, "msg": "数据删除成功"})
#
# # 修改接口，以修改密码为例
# @app.route("/update/", methods=["PUT"])
# def updateApi():
#     userId = request.form.get("id", None)
#     password = request.form.get("password", None)
#
#     _sql = "update `user` set `password` = '{}' where `id` = {}".format(password, userId)
#
#     print(_sql)
#
#     db.session.execute(text(_sql))
#
#     return jsonify({"errcode": 0, "msg": "数据修改成功"})
#
#
# # 插入接口
# @app.route("/insert/", methods=["POST"])
# def insertApi():
#     userId = request.form.get("id", None)
#     email = request.form.get("email", None)
#     password = request.form.get("password", None)
#
#     # 执行插入操作，注意一个问题，mysql里面的表名之类的最好用引号引起来，
#     # 因为如果不引起来的话，有可能会触发mysql中的某些字段，比如有一个order表，
#     # 那么就会合order冲突，这个时候用撇号引起来就可以避免这个问题
#
#     _sql = "insert into `user` (`id`, `email`, `password`) values ({} , '{}', '{}')".format(userId, email, password)
#
#     print(_sql)
#
#     db.session.execute(text(_sql))
#
#     return jsonify({"errcode": 0, "msg": "数据插入成功"})
#
#
# # 配置路由
# @app.route("/", methods=["GET"])
# def index():
#     res = {"msg": "做数据库课设尝试"}
#     # 序列化，原始数据类型转化为json格式
#
#     # 查询所有用户
#     userlist = db.session.execute(text(" select * from user ")).fetchall()
#
#     res = []
#     for item in userlist:
#         data = tuple(item)
#         tmp = {key: value for key, value in zip(['id', 'email', 'password'], data)}
#         res.append(tmp)
#
#     # 插入数据操作
#     db.session.execute(text(" insert into user (id, email, password) values (3, '第三个邮箱', '第三个密码') "))
#
#     # 修改数据
#     db.session.execute(text(" update user set password = '123456' where id = 3"))
#
#     # 删除数据
#     db.session.execute(text(" delete from user where id = 3"))
#
#     res = "good"
#     return jsonify({"data": res})

# 搜狐新闻爬取
def spyderSouHu():
    a = 0
    # 爬取网页，获取数据
    baseurl = "https://www.sohu.com"
    Datalist1, Datalist2, Datalist3, Datalist4, Datalist5, a = getData(baseurl, a)
    # 保存数据
    for i in range(0, a):
        # 新闻标题
        news_title = ''.join('%s' % a for a in Datalist1[i - 1])
        # 新闻文本
        news_content = ''.join('%s' % a for a in Datalist2[i - 1])
        # 新闻链接
        news_url = ''.join('%s' % a for a in Datalist3[i - 1])
        # 新闻热度
        news_hot = ''.join('%s' % a for a in Datalist4[i - 1])
        # 新闻时间
        news_time = ''.join('%s' % a for a in Datalist5[i - 1])
        if news_title == '' or news_content == '':
            continue

        news_time = news_time.split(' ')[0]
        # 先确定是否存在同名的
        _sql = " select `news_id` from `news_bs4` where `news_title` = '{}'".format(
            news_title)
        print(_sql)
        newExist = db.session.execute(text(_sql)).fetchone()
        print(newExist)
        if newExist:
            print("这个文章的标题有相同的")
            continue
        else:
            print("这个文章的标题没有相同的")
            # 确定每次生成的news_id都是唯一的
            while True:
                news_id = str(uuid.uuid1().int >> 64)
                _sql = " select `news_title` from `news_bs4` where `news_id` = '{}'".format(
                    news_id)
                print(_sql)
                newIdExist = db.session.execute(text(_sql)).fetchone()
                if newIdExist:
                    print("这篇文章的id存在")
                    continue
                else:
                    print("这篇文章的id不存在")
                    break
            _sql = "insert into `news_bs4` (`news_id`, `news_title`, `news_source`, `news_time`, `news_content`, `news_url`)" \
                   " values ('{}' , '{}', '{}', '{}', '{}', '{}')".format(news_id, news_title, "搜狐新闻", news_time, news_content, news_url)
            print(_sql)
            db.session.execute(text(_sql))
    print("保存完毕")


def loginUser(user_id, user_password):
    _sql = " select `user_name`, `user_password` from `user_info` where `user_id` = '{}' limit 1".format(
        user_id)
    print(_sql)
    user = db.session.execute(text(_sql)).fetchone()
    if user:
        user = tuple(user)
        user = {key: value for key, value in zip(['user_name', 'user_password'], user)}
        if user_password == user["user_password"]:
            user["user_id"] = user_id
            res = {
                "errcode": 0,  # 匹配成功
                "data": user
            }
        else:
            res = {
                "errcode": 2,  # 匹配此账号密码错误
                "data": {}
            }
    else:
        res = {
            "errcode": 1,  # 代表此账号不存在
            "data": {}
        }
    return res

def loginAdmin(user_id, user_password):
    _sql = " select `user_password` from `user_info` where `user_id` = {} limit 1".format(
        user_id)
    print(_sql)
    admain = db.session.execute(text(_sql)).fetchone()
    admain = tuple(admain)
    admain = {key: value for key, value in zip(['user_password'], admain)}
    if user_password == admain["user_password"]:
        res = {
            "errcode": 0,  # 登录成功
        }
    else:
        res = {
            "errcode": 1,  # 登录密码错误
        }
    return res

# 管理员和用户用同一个接口，根据permission进行比较
# id用来做查询，permission用来做管理员和用户区分，这是因为id很可能管理员人数拓展，因此这样考虑的
@app.route("/login/", methods=["POST"])
def loginApi():
    user_id = request.form.get("user_id", None)
    user_password = request.form.get("user_password", None)
    user_permission = request.form.get("user_permission", None)

    if user_permission == 0:
        res = loginUser(user_id, user_password)
    else:
        res = loginAdmin(user_id,user_password)
    return jsonify(res)


@app.route("/register/", methods=["POST"])
def register():
    user_id = request.form.get("user_id", None)
    user_name = request.form.get("user_name", None)
    user_password = request.form.get("user_password", None)
    user_permission = 0

    # 先查询是否用户存在
    temp = loginUser(user_id, user_password)
    if temp["errcode"] != 1:
        res = {
            "errcode": 1  # 注册失败，用户已经存在
        }
    else:
        _sql = "insert into `user_info` (`user_id`, `user_name`, `user_password`, `user_permission`)" \
               " values ({} , '{}', '{}', {})".format(user_id, user_name, user_password, user_permission)
        print(_sql)
        db.session.execute(text(_sql))
        res = {
            "errcode": 0  # 插入成功
        }
    return res

@app.route("/userSpyder/", methods=["GET"])
def userSpyder():
    spyderSouHu()
    return jsonify({"errcode": "没问题"})


if __name__ == '__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    # add_job() 添加任务
    # 每过12小时，向数据库中添加一次信息
    scheduler.add_job(func=spyderSouHu, args=(), trigger='interval', hours=12, id='interval_task')
    scheduler.start()
    # debug模式开启
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
