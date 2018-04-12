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
    @property
    def db(self):
        return self.application.db
    def get_current_user(self):
        return self.get_secure_cookie('username')
class Tag_ListHandler(AdminHandler):

    @tornado.web.authenticated
    def get(self):
        key = self.get_argument('key', '')
        page = self.get_argument('page', 1)
        page = int(page)
        sql = "select count(*) from tag where name like :key"
        total = self.db.execute(sql, dict(key="%" + key + "%")).fetchone()[0]
        #每页展示个数
        shownum = 10.0
        import math
        #总的页码数
        pagenum = int(math.ceil(total / shownum))
        if pagenum < 1:#如果一页不足10个
            self.redirect(self.request.path + "?page=%d&key=%s" % (1, key))
        if page > pagenum:#如果总页码超过当前页码
            self.redirect(self.request.path + "?page=%d&key=%s" % (pagenum, key))
        offset = (page - 1) * int(shownum)
        sql = "select id,name,addtime from tag where name like :key limit :offset,:limit"
        data = self.db.execute(sql, dict(key="%" + key + "%" ,offset=offset, limit=int(shownum))).fetchall()
        #总共展示的页码数
        pagetotal=5
        #如果不到5页
        if pagenum<pagetotal:
            firstpage=1#第一页
            lastpage=pagenum#最后一页
        else:
            if page==1:
                firstpage=1
                lastpage=pagetotal
            else:
                firstpage=page-2
                lastpage=page+pagetotal-3
                if firstpage<1:
                    firstpage=1
                if lastpage>pagenum:
                    lastpage=pagenum
        prev=page-1
        next=page+1
        if page<1:
            prev=1
        if next>pagenum:
            next=pagenum
        arr=dict(
            pagenum=pagenum,
            total=total,
            prev=prev,
            next=next,
            pagerange=range(firstpage,lastpage+1),
            data=data,
            url=self.request.path,
            key=key,
            page=page,
        )
        self.render('admin/tag_list.html',arr=arr)


class Tag_EditHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id=self.get_argument('id',None)
        if id!=None:
            id=int(id)
            sql="select id,name,info from tag where id= :id"
            tag=self.db.execute(sql,dict(id=id)).fetchone()
            self.db.commit()
            self.db.close()
            self.render('admin/tag_edit.html',tag=tag,id=id)
        else:
            self.render('admin/tag_edit.html',id=id)


    def post(self, *args, **kwargs):
        name=self.get_argument('name',"")
        info=self.get_argument('info',"")
        id =self.get_argument('id',"")
        if id!="":
            id=int(id)
            res=dict(
                ok=1
            )
            if name=="":
                res['ok']=0
                res['name']='标签名称不能空！'
            if info == "":
                res['ok'] = 0
                res['info'] = '标签内容不能空！'

            if res['ok']==1:
                if int(id) == 0:
                    sql="insert into tag(name,info) VALUES ('%s','%s')" %(name,info)
                else:
                    sql = "update tag set name='%s',info='%s' where id=%d" %(name,info,int(id))
                self.db.execute(sql)
                self.db.commit()
                self.db.close()
            self.set_header('content-type','application/json')
            self.write(json.dumps(res))

class TagdelHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self):
        id =self.get_argument('id')
        id =int(id)
        sql="delete from tag where id=:id"
        self.db.execute(sql,dict(id=id))
        self.db.commit()
        self.db.close()
        self.redirect('/tag_list.html')



class Art_ListHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('admin/art_list.html')

class Art_EditHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        sql="select * from tag"
        data=self.db.execute(sql).fetchall()
        self.render('admin/art_edit.html',data=data)

class UploadHandler(AdminHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        res=dict(ok=1)
        self.set_header('content-type','application/json')
        self.write(json.dumps(res))