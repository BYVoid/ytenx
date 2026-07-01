# coding=utf-8
import ytenx.trngyan.views
from django.urls import re_path

urlpatterns = [
  re_path(r'^$', ytenx.trngyan.views.triung_ngyan_qim_yonh, name='triung_ngyan_qim_yonh'),
  re_path(r'^sieux/$', ytenx.trngyan.views.sieux_yonh_pieux, name='trngyan-sieux_yonh_pieux'),
  re_path(r'^sieux/(\d{1,4})/$', ytenx.trngyan.views.sieux_yonh, name='trngyan-sieux_yonh'),
  re_path(r'^dzih/$', ytenx.trngyan.views.dzih_pieux, name='trngyan-dzih_pieux'),
  re_path(r'^dzih/(.+)/$', ytenx.trngyan.views.dzih, name='trngyan-dzih'),
  re_path(r'^cjeng/$', ytenx.trngyan.views.cjeng_mux_pieux, name='trngyan-cjeng_mux_pieux'),
  re_path(r'^cjeng/(.+)/$', ytenx.trngyan.views.cjeng_mux, name='trngyan-cjeng_mux'),
  re_path(r'^yonh/$', ytenx.trngyan.views.yonh_mux_pieux, name='trngyan-yonh_mux_pieux'),
  re_path(r'^yonh/(.+)/$', ytenx.trngyan.views.yonh_mux, name='trngyan-yonh_mux'),
  re_path(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.trngyan.views.cio, name='trngyan-cio'),
]
