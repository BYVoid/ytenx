# coding=utf-8
import ytenx.kyonh.views
from django.conf.urls import url

urlpatterns = [
  url(r'^intro$', ytenx.kyonh.views.intro_page),
  url(r'^sieux$', ytenx.kyonh.views.sieux_yonh_list_page, name='kyonh-sieux_yonh_list_page'),
  url(r'^sieux/(\d{1,4})/$', ytenx.kyonh.views.sieux_yonh_page, name='kyonh-sieux_yonh_page'),
  url(r'^dzih$', ytenx.kyonh.views.dzih_pieux, name='kyonh-dzih_pieux'),
  url(r'^dzih/(\d{1,5})/$', ytenx.kyonh.views.dzih, name='kyonh-dzih'),
  url(r'^cjeng$', ytenx.kyonh.views.cjeng_mux_list_page, name='kyonh-cjeng_mux_list_page'),
  url(r'^cjeng/(.+)/$', ytenx.kyonh.views.cjeng_mux_page, name='kyonh-cjeng_mux_page'),
  url(r'^yonh$', ytenx.kyonh.views.yonh_mux_list_page, name='kyonh-yonh_mux_list_page'),
  url(r'^yonh/(.+)/$', ytenx.kyonh.views.yonh_mux_page, name='kyonh-yonh_mux_page'),
  url(r'^yonhmiuk$', ytenx.kyonh.views.yonh_miuk_list_page, name='kyonh-yonh_miuk_list_page'),
  url(r'^yonhmiuk/(.+)/$', ytenx.kyonh.views.yonh_miuk_page, name='kyonh-yonh_miuk_page'),
  url(r'^cjengngix$', ytenx.kyonh.views.cjeng_ngix_list_page, name='kyonh-cjeng_ngix_list_page'),
  url(r'^yonhngix$', ytenx.kyonh.views.yonh_ngix_list_page, name='kyonh-yonh_ngix_list_page'),
  url(r'^yonhdo$', ytenx.kyonh.views.yonh_do_page, name='kyonh-yonh_do_page'),
  url(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.kyonh.views.cio_page, name='kyonh-cio_page'),
  url(r'^pyanx/dciangx/(.+)/$', ytenx.kyonh.views.pyanx_dciangx_page, name='kyonh-pyanx_dciangx_page'),
  url(r'^pyanx/ghrax/(.+)/$', ytenx.kyonh.views.pyanx_ghrax_page, name='kyonh-pyanx_ghrax_page'),
  url(r'^$', ytenx.kyonh.views.index_page, name='kyonh'),
]
