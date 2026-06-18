# coding=utf-8
import ytenx.kyonh.views
from django.urls import re_path

urlpatterns = [
  re_path(r'^intro$', ytenx.kyonh.views.intro_page),
  re_path(r'^sieux$', ytenx.kyonh.views.sieux_yonh_list_page, name='kyonh-sieux_yonh_list_page'),
  re_path(r'^sieux/(\d{1,4})/$', ytenx.kyonh.views.sieux_yonh_page, name='kyonh-sieux_yonh_page'),
  re_path(r'^dzih$', ytenx.kyonh.views.dzih_pieux, name='kyonh-dzih_pieux'),
  re_path(r'^dzih/(\d{1,5})/$', ytenx.kyonh.views.dzih, name='kyonh-dzih'),
  re_path(r'^cjeng$', ytenx.kyonh.views.cjeng_mux_list_page, name='kyonh-cjeng_mux_list_page'),
  re_path(r'^cjeng/(.+)/$', ytenx.kyonh.views.cjeng_mux_page, name='kyonh-cjeng_mux_page'),
  re_path(r'^yonh$', ytenx.kyonh.views.yonh_mux_list_page, name='kyonh-yonh_mux_list_page'),
  re_path(r'^yonh/(.+)/$', ytenx.kyonh.views.yonh_mux_page, name='kyonh-yonh_mux_page'),
  re_path(r'^yonhmiuk$', ytenx.kyonh.views.yonh_miuk_list_page, name='kyonh-yonh_miuk_list_page'),
  re_path(r'^yonhmiuk/(.+)/$', ytenx.kyonh.views.yonh_miuk_page, name='kyonh-yonh_miuk_page'),
  re_path(r'^cjengngix$', ytenx.kyonh.views.cjeng_ngix_list_page, name='kyonh-cjeng_ngix_list_page'),
  re_path(r'^yonhngix$', ytenx.kyonh.views.yonh_ngix_list_page, name='kyonh-yonh_ngix_list_page'),
  re_path(r'^yonhdo$', ytenx.kyonh.views.yonh_do_page, name='kyonh-yonh_do_page'),
  re_path(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.kyonh.views.cio_page, name='kyonh-cio_page'),
  re_path(r'^pyanx/dciangx/(.+)/$', ytenx.kyonh.views.pyanx_dciangx_page, name='kyonh-pyanx_dciangx_page'),
  re_path(r'^pyanx/ghrax/(.+)/$', ytenx.kyonh.views.pyanx_ghrax_page, name='kyonh-pyanx_ghrax_page'),
  re_path(r'^$', ytenx.kyonh.views.index_page, name='kyonh'),
]
