# _*_ coding:utf-8 _*_
__author__ = 'xuyijie'
__date__ = '2018/4/11 上午10:19'
import os
base_dir=os.path.dirname(__file__)
configs=dict(
    template_path=os.path.join(base_dir,'templates'),
    static_path=os.path.join(base_dir,'static'),
    debug=True,
    xsrf_cookies=True,
    cookie_secret='b20d54324b0f4a77a5b4388393339b20',
    login_url='login.html'
)