# coding=utf-8
import ytenx.pyonh.views
from django.conf.urls import url

urlpatterns = [
  url(r'^$', ytenx.pyonh.views.pyon_yonh, name='pyon_yonh'),
  url(r'^sieux$', ytenx.pyonh.views.sieux_yonh_pieux, name='pyon_yonh-sieux_yonh_pieux'),
  url(r'^sieux/(\d{1,4})/$', ytenx.pyonh.views.sieux_yonh, name='pyon_yonh-sieux_yonh'),
  url(r'^dzih$', ytenx.pyonh.views.dzih_pieux, name='pyon_yonh-dzih_pieux'),
  url(r'^dzih/(\d{1,4})/$', ytenx.pyonh.views.dzih, name='pyon_yonh-dzih'),
  url(r'^cjeng$', ytenx.pyonh.views.cjeng_mux_pieux, name='pyon_yonh-cjeng_mux_pieux'),
  url(r'^cjeng/(.+)/$', ytenx.pyonh.views.cjeng_mux, name='pyon_yonh-cjeng_mux'),
  url(r'^yonh$', ytenx.pyonh.views.yonh_mux_pieux, name='pyon_yonh-yonh_mux_pieux'),
  url(r'^yonh/(.+)/$', ytenx.pyonh.views.yonh_mux, name='pyon_yonh-yonh_mux'),
  url(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.pyonh.views.cio, name='pyon_yonh-cio'),
]
