# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/4/11 上午10:20'
import tornado.web
class HomeHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
class IndexHandler(HomeHandler):
    def get(self, *args, **kwargs):
        url=self.request.path
        sql="select id,name from tag"
        tags=self.db.execute(sql).fetchall()

        t=self.get_argument('t',0)
        t=int(t)

        key = self.get_argument('key', '')
        page = self.get_argument('page', 1)
        page = int(page)
        sql = "select count(*) from art "
        #总条数
        total = self.db.execute(sql).fetchone()[0]
        if total>0:
            shownum=20
            import math
            # 总的页码数
            pagenum = int(math.ceil(total / shownum))

            if pagenum < 1:  # 如果一页不足10个
                self.redirect(self.request.path + "?page=%d&key=%s" % (1, key))
            if page > pagenum:  # 如果总页码超过当前页码
                self.redirect(self.request.path + "?page=%d&key=%s" % (pagenum, key))
            offset = (page - 1) * int(shownum)
            if t==0:
                sql = "select a.id,a.title,a.info,a.content,a.img,a.addtime from art as a limit :offset,:limit"
                data = self.db.execute(sql,
                                       dict(offset=offset, limit=int(shownum))).fetchall()
            else:
                sql = "select a.id,a.title,a.info,a.content,a.img,a.addtime from art as a  where  a.tag=:tag limit :offset,:limit"
                data = self.db.execute(sql, dict(tag=t, offset=offset, limit=int(shownum))).fetchall()
            # 总共展示的页码数
            pagetotal = 5
            # 如果不到5页
            if pagenum < pagetotal:
                firstpage = 1  # 第一页
                lastpage = pagenum  # 最后一页
            else:
                if page == 1:
                    firstpage = 1
                    lastpage = pagetotal
                else:
                    firstpage = page - 2
                    lastpage = page + pagetotal - 3
                    if firstpage < 1:
                        firstpage = 1
                    if lastpage > pagenum:
                        lastpage = pagenum
            prev = page - 1
            next = page + 1
            if page < 1:
                prev = 1
            if next > pagenum:
                next = pagenum
            arr = dict(
                url=url,
                tags=tags,
                pagenum=pagenum,
                total=total,
                prev=prev,
                next=next,
                pagerange=range(firstpage, lastpage + 1),
                data=data,
                key=key,
                page=page,
                t=t,
            )
            self.render('home/index.html',arr=arr)


class SearchHanlder(HomeHandler):
    def get(self, *args, **kwargs):
        keysearch=self.get_argument('key')
        key = self.get_argument('key', '')
        page = self.get_argument('page', 1)
        url = self.request.path
        page = int(page)
        sql = "select count(*) from art "
        # 总条数
        total = self.db.execute(sql).fetchone()[0]
        if total > 0:
            shownum = 20
            import math
            # 总的页码数
            pagenum = int(math.ceil(total / shownum))

            if pagenum < 1:  # 如果一页不足10个
                self.redirect(self.request.path + "?page=%d&key=%s" % (1, key))
            if page > pagenum:  # 如果总页码超过当前页码
                self.redirect(self.request.path + "?page=%d&key=%s" % (pagenum, key))
            offset = (page - 1) * int(shownum)

            sql = "select a.id,a.title,a.info,a.content,a.img,a.addtime from art as a where a.title like :key or a.content like :key or a.info like :key limit :offset,:limit"
            data = self.db.execute(sql,
                                       dict(key="%" + keysearch + "%", offset=offset, limit=int(shownum))).fetchall()
            # 总共展示的页码数
            pagetotal = 5
            # 如果不到5页
            if pagenum < pagetotal:
                firstpage = 1  # 第一页
                lastpage = pagenum  # 最后一页
            else:
                if page == 1:
                    firstpage = 1
                    lastpage = pagetotal
                else:
                    firstpage = page - 2
                    lastpage = page + pagetotal - 3
                    if firstpage < 1:
                        firstpage = 1
                    if lastpage > pagenum:
                        lastpage = pagenum
            prev = page - 1
            next = page + 1
            if page < 1:
                prev = 1
            if next > pagenum:
                next = pagenum
            arr = dict(
                pagenum=pagenum,
                total=total,
                prev=prev,
                next=next,
                pagerange=range(firstpage, lastpage + 1),
                data=data,
                key=key,
                page=page,
                url=url,
            )
            self.render('home/search.html', arr=arr)


class DetailHanlder(HomeHandler):
    def get(self, *args, **kwargs):
        id=self.get_argument('id',None)
        if id==None:
            self.redirect('/')
        sql="select title,info,content,img from art where art.id=%s"%id
        data=self.db.execute(sql).fetchone()
        self.db.commit()
        self.db.close()
        self.render('home/detail.html',data=data)
