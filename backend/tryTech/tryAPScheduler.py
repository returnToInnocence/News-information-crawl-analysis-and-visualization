from flask import Flask
from flask_apscheduler import APScheduler
import time


class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 添加API

scheduler = APScheduler()


def task1(x):
    print(f'task 1 executed --------: {x}', time.time())


def task2(x):
    print(f'task 2 executed --------: {x}', time.time())


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())
    scheduler.init_app(app)
    # add_job() 添加任务
    scheduler.add_job(func=task1, args=('循环',), trigger='interval', minutes=1, id='interval_task')
    # scheduler.add_job(func=task2, args=('定时任务',), trigger='cron', second='*/10', id='cron_task')
    scheduler.start()
    app.run(use_reloader=False)