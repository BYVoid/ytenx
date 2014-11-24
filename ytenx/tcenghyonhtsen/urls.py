# coding=utf-8
from django.conf.urls import patterns

urlpatterns = patterns('',
  (r'^sync$', 'ytenx.tcenghyonhtsen.sync.sync'),
  (r'^sieux$', 'ytenx.tcenghyonhtsen.views.sieux_yonh_list_page'),
  (r'^sieux/(\d{1,4})/$', 'ytenx.tcenghyonhtsen.views.sieux_yonh_page'),
  (r'^yonhmiuk$', 'ytenx.tcenghyonhtsen.views.yonh_miuk_list_page'),
  (r'^yonhmiuk/(.+)/$', 'ytenx.tcenghyonhtsen.views.yonh_miuk_page'),
  (r'^cio/(\d{1,1})/(\d{1,3})/$', 'ytenx.tcenghyonhtsen.views.cio_page'),
  (r'^$', 'ytenx.tcenghyonhtsen.views.index_page'),
)
