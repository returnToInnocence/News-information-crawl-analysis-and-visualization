# 项目入口文件
import time
import uuid

from flask import Flask, jsonify, request, current_app, config, copy_current_request_context

# 解决浏览器同源策略导致的跨域问题
from flask_cors import CORS

# 解决string SQL 由warning 变成了 Coercion的问题
from sqlalchemy.sql import text

# 导入数据库实例
from database import db

# 导入数据库配置
from config import *

from spyder import spyderSouhu

# 引入定时器，用来定时对网站进行爬取，以二十四小时为时间
from flask_apscheduler import APScheduler

from myLib import createId

from aiLib import BD_txt_main, BD_classify, BD_keyword, paint_hot_click, Word_cloud

import csv



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



@app.route("/getArticle/", methods=["POST"])
def getArticle():
    # 返回值应该是
    # - 新闻标题 ok
    # - 新闻摘要 ok
    # - 新闻分类
    # - 新闻关键词
    # 所以这个功能想要实现的话，首先要用ai接口生成对应的内容才行
    pass


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
        res = loginAdmin(user_id, user_password)
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

# 填充分类字段，两个表一个根据分类结果查询id，
def fillClassify():
    _sql = "SELECT `news_id`, `news_title`, `news_content` FROM news_bs4"
    newsRowList = db.session.execute(text(_sql)).fetchall()
    newsList = []
    for item in newsRowList:
        data = tuple(item)
        tmp = {key: value for key, value in zip(['news_id', 'news_title', 'news_content'], data)}
        newsList.append(tmp)
    for item in newsList:
        if len(item["news_title"]) < 40 and len(item["news_title"]) > 0:
            print(item["news_id"])
            text_classify = BD_classify.classify(item["news_content"], item["news_title"])
            print(text_classify)
            # 查询分类的id
            _sql = "SELECT `classification_id` FROM `news_classification` WHERE `news_classification` = '{}'".format(text_classify)
            classify_id = db.session.execute(text(_sql)).fetchone()
            classify_id = classify_id[0]
            # print(classify_id)
            # print(type(classify_id))
            _sql = "UPDATE `news_bs4` set `classification_id` = {} WHERE `news_id` = '{}'".format(classify_id, item["news_id"])
            db.session.execute(text(_sql))
            print("完成一条更新")
            time.sleep(0.5)


# 数据库summary字段填充，就一直用这个方法吧，先不优化了，实现功能优先
# @app.route("/fillSummary/", methods=["GET"])
def fillSummary():
    _sql = "SELECT `news_id`, `news_title`, `news_content` FROM news_bs4"
    newsRowList = db.session.execute(text(_sql)).fetchall()
    newsList = []
    for item in newsRowList:
        data = tuple(item)
        tmp = {key: value for key, value in zip(['news_id', 'news_title', 'news_content'], data)}
        newsList.append(tmp)
    for item in newsList:
        if len(item["news_content"]) < 2900 and len(item["news_content"]) > 20:
            text_main = BD_txt_main.txt_main(item["news_title"], item["news_content"])
            print(text_main)
            _sql = "UPDATE `news_bs4` set `news_summary` = '{}' WHERE `news_id` = '{}'".format(text_main, item["news_id"])
            db.session.execute(text(_sql))
            print("完成一条更新")
            time.sleep(0.5)
    # return jsonify({"errcode": 0})


# 删除旧数据，加入新数据
# 这里删除的内容就是包括news_info的所有数据
# 所有关键字数据
# 所有关键字关联表数据
def deletAll():
    # 删除news_bs4表种所有数据
    _sql = "DELETE FROM `news_bs4`"
    db.session.execute(text(_sql))
    _sql = "DELETE FROM `news_keyword`"
    db.session.execute(text(_sql))
    _sql = "DELETE FROM `keyword_and_news`"
    db.session.execute(text(_sql))


# 搜狐新闻爬取
def spyderSouHu():
    a = 0
    # 爬取网页，获取数据
    baseurl = "https://www.sohu.com"
    Datalist1, Datalist2, Datalist3, Datalist4, Datalist5, a = spyderSouhu.getData(baseurl, a)
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
        # print(newExist)
        if newExist:
            print("这个文章的标题有相同的")

            continue
        else:
            print("这个文章的标题没有相同的")
            # 确定每次生成的news_id都是唯一的
            while True:
                # id生成采用自己设计的id生成方式来做
                news_id = createId.get_short_id()
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
            # 为了ai算法模型能够正常使用，因此加入的一些判断条件
            if len(news_content) < 2900 and len(news_content) > 20 and len(news_title) < 40 and len(news_title) > 0:
                _sql = "insert into `news_bs4` (`news_id`, `news_title`, `news_source_name`, `news_time`, `news_content`, `news_url`, `news_fever`)" \
                                       " values ('{}' , '{}', '{}', '{}', '{}', '{}', {})".format(news_id, news_title, "搜狐新闻", news_time,
                                                                                          news_content, news_url, news_hot)
                print(_sql)
                db.session.execute(text(_sql))
    print("保存完毕")




def fillKeyWord():
    # 不需要文章的名字
    _sql = "SELECT `news_id`, `news_content` FROM news_bs4"
    newsRowList = db.session.execute(text(_sql)).fetchall()
    newsList = []
    for item in newsRowList:
        data = tuple(item)
        tmp = {key: value for key, value in zip(['news_id',  'news_content'], data)}
        newsList.append(tmp)
    # 会 保存所有的关键词
    allKeyWord = []
    for item in newsList:
        text_keyWord = BD_keyword.analyze(item["news_content"])
        print(text_keyWord)
        for keyWord in text_keyWord:
            _sql = "insert into `keyword_and_news` (`news_id`, `news_keyWord`) values ('{}', '{}')".format(
                item["news_id"], keyWord)
            db.session.execute(text(_sql))
        allKeyWord = allKeyWord + text_keyWord
    dictKeyWord = {}
    for key in allKeyWord:
        dictKeyWord[key] = dictKeyWord.get(key, 0) + 1
    print(dictKeyWord)
    for key in dictKeyWord:
        # 插入keyword表
        _sql = "insert into `news_keyword`(`news_keyWord`, `times`) values ('{}', {})".format(key, dictKeyWord[key])
        db.session.execute(text(_sql))
        # time.sleep(0.5)


# 基本数据获取与保存，整套流程
# @app.route("/basicDataSave/", methods=["GET"])
def basicDataSave():
    deletAll()
    # 搜狐新闻爬取数据并保存到数据库
    spyderSouHu()
    # # 文本概要提取
    fillSummary()
    # 文本分类设定
    fillClassify()
    # 文本关键词提取和三个数据库的保存
    fillKeyWord()
    return jsonify({})


def imageSave(filename):
    image = ""  # 假设这里是一个图片
    image_path = os.path.join(current_app.config['IMAGE_SAVE_PATH'], filename)
    # 图片保存
    image.save(image_path)
    # 把imagepath+/filename保存到数据库


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

    # 现在调试的时候先不启动计时器
    # 感觉有点浪费资源

    # app.config.from_object(Config())
    # scheduler.init_app(app)
    # # add_job() 添加任务
    # # 每过12小时，向数据库中添加一次信息
    # scheduler.add_job(func=basicDataSave, args=(), trigger='interval', hours=12, id='interval_task')
    # scheduler.start()
    # # debug模式开启
    # app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
