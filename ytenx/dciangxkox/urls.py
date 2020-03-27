# coding=utf-8
import ytenx.dciangxkox.views
from django.conf.urls import url

urlpatterns = [
  url(r'^$', ytenx.dciangxkox.views.dciangx_kox, name='dciangx_kox'),
  url(r'^dzih/$', ytenx.dciangxkox.views.dzih_pieux, name='dciangx_kox-dzih_pieux'),
  url(r'^dzih/(.+)/$', ytenx.dciangxkox.views.dzih, name='dciangx_kox-dzih'),
  url(r'^cjeng/$', ytenx.dciangxkox.views.cjeng_byo_pieux, name='dciangx_kox-cjeng_byo_pieux'),
  url(r'^cjeng/(.+)/$', ytenx.dciangxkox.views.cjeng_byo, name='dciangx_kox-cjeng_byo'),
  url(r'^yonh/$', ytenx.dciangxkox.views.yonh_box_pieux, name='dciangx_kox-yonh_box_pieux'),
  url(r'^yonh/(.+)/$', ytenx.dciangxkox.views.yonh_box, name='dciangx_kox-yonh_box'),
]
