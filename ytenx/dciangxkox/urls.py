# coding=utf-8
import ytenx.dciangxkox.views
from django.urls import re_path

urlpatterns = [
  re_path(r'^$', ytenx.dciangxkox.views.dciangx_kox, name='dciangx_kox'),
  re_path(r'^dzih/$', ytenx.dciangxkox.views.dzih_pieux, name='dciangx_kox-dzih_pieux'),
  re_path(r'^dzih/(.+)/$', ytenx.dciangxkox.views.dzih, name='dciangx_kox-dzih'),
  re_path(r'^cjeng/$', ytenx.dciangxkox.views.cjeng_byo_pieux, name='dciangx_kox-cjeng_byo_pieux'),
  re_path(r'^cjeng/(.+)/$', ytenx.dciangxkox.views.cjeng_byo, name='dciangx_kox-cjeng_byo'),
  re_path(r'^yonh/$', ytenx.dciangxkox.views.yonh_box_pieux, name='dciangx_kox-yonh_box_pieux'),
  re_path(r'^yonh/(.+)/$', ytenx.dciangxkox.views.yonh_box, name='dciangx_kox-yonh_box'),
]
