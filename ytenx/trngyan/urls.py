# coding=utf-8
import ytenx.trngyan.views
from django.conf.urls import url

urlpatterns = [
  url(r'^$', ytenx.trngyan.views.triung_ngyan_qim_yonh, name='triung_ngyan_qim_yonh'),
  url(r'^sieux/$', ytenx.trngyan.views.sieux_yonh_pieux, name='trngyan-sieux_yonh_pieux'),
  url(r'^sieux/(\d{1,4})/$', ytenx.trngyan.views.sieux_yonh, name='trngyan-sieux_yonh'),
  url(r'^dzih/$', ytenx.trngyan.views.dzih_pieux, name='trngyan-dzih_pieux'),
  url(r'^dzih/(.+)/$', ytenx.trngyan.views.dzih, name='trngyan-dzih'),
  url(r'^cjeng/$', ytenx.trngyan.views.cjeng_mux_pieux, name='trngyan-cjeng_mux_pieux'),
  url(r'^cjeng/(.+)/$', ytenx.trngyan.views.cjeng_mux, name='trngyan-cjeng_mux'),
  url(r'^yonh/$', ytenx.trngyan.views.yonh_mux_pieux, name='trngyan-yonh_mux_pieux'),
  url(r'^yonh/(.+)/$', ytenx.trngyan.views.yonh_mux, name='trngyan-yonh_mux'),
  url(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.trngyan.views.cio, name='trngyan-cio'),
]
