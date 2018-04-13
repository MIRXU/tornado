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
        arr=dict(
            url=url,
            tags=tags
        )
        t=self.get_argument('t')

        key = self.get_argument('key', '')
        page = self.get_argument('page', 1)
        page = int(page)
        sql = "select count(*) from art where title like :key or content like :key or info like :key"
        total = self.db.execute(sql, dict(key="%" + key + "%")).fetchone()[0]
        # 每页展示个数
        shownum = 10.0
        import math
        # 总的页码数
        pagenum = int(math.ceil(total / shownum))
        if pagenum < 1:  # 如果一页不足10个
            self.redirect(self.request.path + "?page=%d&key=%s" % (1, key))
        if page > pagenum:  # 如果总页码超过当前页码
            self.redirect(self.request.path + "?page=%d&key=%s" % (pagenum, key))
        offset = (page - 1) * int(shownum)
        sql = "select a.id,a.title,a.img,t.name,a.addtime from art as a left join tag as t on a.tag=t.id where a.title like :key or a.content like :key or a.info like :key limit :offset,:limit"
        data = self.db.execute(sql, dict(key="%" + key + "%", offset=offset, limit=int(shownum))).fetchall()
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
            url=self.request.path,
            key=key,
            page=page,
        )
        self.render('home/index.html',arr=arr)


class SearchHanlder(HomeHandler):
    def get(self, *args, **kwargs):
        self.render('home/search.html')


class DetailHanlder(HomeHandler):
    def get(self, *args, **kwargs):
        self.render('home/detail.html')
