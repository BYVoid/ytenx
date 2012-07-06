# coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
  (r'^$', 'ytenx.trngyan.views.triung_ngyan_qim_yonh'),
  (r'^sieux/$', 'ytenx.trngyan.views.sieux_yonh_pieux'),
  (r'^sieux/(\d{1,4})/$', 'ytenx.trngyan.views.sieux_yonh'),
  (r'^dzih/$', 'ytenx.trngyan.views.dzih_pieux'),
  (r'^dzih/(.+)/$', 'ytenx.trngyan.views.dzih'),
  (r'^cjeng/$', 'ytenx.trngyan.views.cjeng_mux_pieux'),
  (r'^cjeng/(.+)/$', 'ytenx.trngyan.views.cjeng_mux'),
  (r'^yonh/$', 'ytenx.trngyan.views.yonh_mux_pieux'),
  (r'^yonh/(.+)/$', 'ytenx.trngyan.views.yonh_mux'),
  (r'^cio/(\d{1,1})/(\d{1,3})/$', 'ytenx.trngyan.views.cio'),
)
