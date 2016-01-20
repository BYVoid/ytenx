# coding=utf-8
from django.conf.urls import patterns
from django.conf import settings

urlpatterns = patterns('',
  (r'^$', 'ytenx.pyonh.views.pyon_yonh'),
  (r'^sieux$', 'ytenx.pyonh.views.sieux_yonh_pieux'),
  (r'^sieux/(\d{1,4})/$', 'ytenx.pyonh.views.sieux_yonh'),
  (r'^dzih$', 'ytenx.pyonh.views.dzih_pieux'),
  (r'^dzih/(\d{1,4})/$', 'ytenx.pyonh.views.dzih'),
  (r'^cjeng$', 'ytenx.pyonh.views.cjeng_mux_pieux'),
  (r'^cjeng/(.+)/$', 'ytenx.pyonh.views.cjeng_mux'),
  (r'^yonh$', 'ytenx.pyonh.views.yonh_mux_pieux'),
  (r'^yonh/(.+)/$', 'ytenx.pyonh.views.yonh_mux'),
  (r'^cio/(\d{1,1})/(\d{1,3})/$', 'ytenx.pyonh.views.cio'),
)

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^sync$', 'ytenx.pyonh.sync.sync'),
  )
