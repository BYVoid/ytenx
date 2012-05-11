# coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
  (r'^sync$', 'ytenx.kyonh.sync.sync'),
  (r'^intro$', 'ytenx.kyonh.views.intro_page'),
  (r'^sieux$', 'ytenx.kyonh.views.sieux_yonh_list_page'),
  (r'^sieux/(\d{1,4})/$', 'ytenx.kyonh.views.sieux_yonh_page'),
  (r'^cjeng$', 'ytenx.kyonh.views.cjeng_mux_list_page'),
  (r'^cjeng/(.+)/$', 'ytenx.kyonh.views.cjeng_mux_page'),
  (r'^yonh$', 'ytenx.kyonh.views.yonh_mux_list_page'),
  (r'^yonh/(.+)/$', 'ytenx.kyonh.views.yonh_mux_page'),
  (r'^yonhmiuk$', 'ytenx.kyonh.views.yonh_miuk_list_page'),
  (r'^yonhmiuk/(.+)/$', 'ytenx.kyonh.views.yonh_miuk_page'),
  (r'^cjengngix$', 'ytenx.kyonh.views.cjeng_ngix_list_page'),
  (r'^yonhngix$', 'ytenx.kyonh.views.yonh_ngix_list_page'),
  (r'^yonhdo$', 'ytenx.kyonh.views.yonh_do_page'),
  (r'^cio/(\d{1,1})/(\d{1,3})/$', 'ytenx.kyonh.views.cio_page'),
  (r'^$', 'ytenx.kyonh.views.index_page'),
)
