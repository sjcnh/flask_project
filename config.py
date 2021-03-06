#encoding: utf-8
import os

#debug
DEBUG = True

#salt
SECRET_KEY = os.urandom(24)

#数据库
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'syqa'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST
                                                                       , PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False