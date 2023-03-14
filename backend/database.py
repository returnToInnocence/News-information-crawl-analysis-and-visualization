# 数据库实例
from flask_sqlalchemy import SQLAlchemy

# 模拟db
import pymysql

pymysql.install_as_MySQLdb()

# 实例化mysql对象
db = SQLAlchemy()
