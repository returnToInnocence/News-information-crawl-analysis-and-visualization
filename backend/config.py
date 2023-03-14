# 抽取出来一些配置，抽取的目标是一些动态可能发生变更的内容进行抽取
import os

mysqlUser = "LiHongJun"
mysqlPassword = "Shujuku2002"
mysqlHost = "sh-cynosdbmysql-grp-hdc5p1zy.sql.tencentcdb.com"
mysqlPort = 23000
mysqlDb = "databasedesign"

# 项目根路径
BASE_DIR = os.path.dirname(__file__)

# 自动在本地创建一个文件夹配置
IMAGE_SAVE_PATH = os.path.join(BASE_DIR, 'sources', 'image')