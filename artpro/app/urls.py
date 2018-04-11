# _*_ coding:utf-8 _*_
__author__='xuyijie'
__date__='2018/4/11 上午10:19'
from home.views import IndexHandler as home_index
from home.views import SearchHanlder as home_search
from home.views import DetailHanlder as home_detail
from admin.views import LoginHandler as admin_login
from admin.views import Tag_ListHandler as admin_tag_list
from admin.views import Tag_EditHandler as admin_tag_edit
from admin.views import Art_ListHandler as admin_art_list
from admin.views import Art_EditHandler as admin_art_edit
from admin.views import LogoutHandler as admin_logout

urls=[
    (r'/',home_index),
    (r'/index\.html',home_index),
    (r'/search\.html',home_search),
    (r'/detail\.html',home_detail),
    (r'/login\.html',admin_login),
    (r'/tag_list\.html',admin_tag_list),
    (r'/tag_edit\.html',admin_tag_edit),
    (r'/art_list\.html',admin_art_list),
    (r'/art_edit\.html',admin_art_edit),
    (r'/logout\.html',admin_logout),
]