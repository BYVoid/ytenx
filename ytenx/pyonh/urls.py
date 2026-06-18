# coding=utf-8
import ytenx.pyonh.views
from django.urls import re_path

urlpatterns = [
  re_path(r'^$', ytenx.pyonh.views.pyon_yonh, name='pyon_yonh'),
  re_path(r'^sieux$', ytenx.pyonh.views.sieux_yonh_pieux, name='pyon_yonh-sieux_yonh_pieux'),
  re_path(r'^sieux/(\d{1,4})/$', ytenx.pyonh.views.sieux_yonh, name='pyon_yonh-sieux_yonh'),
  re_path(r'^dzih$', ytenx.pyonh.views.dzih_pieux, name='pyon_yonh-dzih_pieux'),
  re_path(r'^dzih/(\d{1,4})/$', ytenx.pyonh.views.dzih, name='pyon_yonh-dzih'),
  re_path(r'^cjeng$', ytenx.pyonh.views.cjeng_mux_pieux, name='pyon_yonh-cjeng_mux_pieux'),
  re_path(r'^cjeng/(.+)/$', ytenx.pyonh.views.cjeng_mux, name='pyon_yonh-cjeng_mux'),
  re_path(r'^yonh$', ytenx.pyonh.views.yonh_mux_pieux, name='pyon_yonh-yonh_mux_pieux'),
  re_path(r'^yonh/(.+)/$', ytenx.pyonh.views.yonh_mux, name='pyon_yonh-yonh_mux'),
  re_path(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.pyonh.views.cio, name='pyon_yonh-cio'),
]
