# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/4/11 上午10:20'
import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('home/index.html')


class SearchHanlder(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('home/search.html')


class DetailHanlder(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('home/detail.html')
