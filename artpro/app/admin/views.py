# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/4/11 上午10:21'
import tornado.web
import json


class LoginHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get(self, *args, **kwargs):
        self.render('admin/login.html')
    def post(self, *args, **kwargs):
        name=self.get_argument('name',"")
        pwd=self.get_argument('pwd',"")
        print "-----"+name
        res=dict(
            ok=1
        )
        if name == "":
            res['ok']=0
            res['name']='管理员名称不能为空'
        if pwd == "":
            res['ok']=0
            res['pwd']='管理员密码不能为空'
        if res['ok']==1:
            import hashlib
            up=hashlib.md5()
            up.update(pwd)
            pwd=up.hexdigest()
            sql="select count(*) from admin where name='%s' and pad ='%s'"%(name,pwd)
            count =self.db.execute(sql).fetchone()
            if count[0]==0:
                res['ok']=0
                res['pwd']='账号或者密码错误'
            else:
                self.set_secure_cookie('username',name)
            self.set_header('content-type','application/json')
            self.write(json.dumps(res))

class LogoutHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie('username')
        self.redirect('/login.html')

class AdminHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')
class Tag_ListHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/tag_list.html')

class Tag_EditHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/tag_edit.html')


class Art_ListHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/art_list.html')

class Art_EditHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/art_edit.html')