# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/4/11 上午10:19'
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import options,define

from configs import configs
from urls import urls
define('port',type=int,default=8000)
define('db_host',type=str,default='127.0.0.1')
define('db_user',type=str,default='root')
define('db_pwd',type=str,default='root')
define('db_name',type=str,default='artdb')
define('db_port',type=int,default=3306)

from sqlalchemy import create_engine
import pymysql
from sqlalchemy.orm import scoped_session,sessionmaker
engine=create_engine(
    'mysql+pymysql://%s:%s@%s:%d/%s' %(
        options.db_user,
        options.db_pwd,
        options.db_host,
        options.db_port,
        options.db_name,

    ),
    encoding='utf-8',
    echo=False,
    pool_size=100,
    pool_recycle=7200,
    connect_args={'charset': 'utf8'}
)
class CustomApplication(tornado.web.Application):
   def __init__(self,cofig,urls):
       setting=configs
       handlers=urls
       super(CustomApplication,self).__init__(handlers=handlers,**setting)
       self.db=scoped_session(
           sessionmaker(
               bind=engine,
               autocommit=False,
               autoflush=True,
               expire_on_commit=False
           )
       )


def creat_app():
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(CustomApplication(configs,urls))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

app=creat_app()