# coding=utf-8
import ytenx
from django.urls import re_path
from ytenx.tcenghyonhtsen.views import *

urlpatterns = [
  re_path(r'^sieux$', ytenx.tcenghyonhtsen.views.sieux_yonh_list_page, name='tcenghyonhtsen-sieux_yonh_list_page'),
  re_path(r'^sieux/(\d{1,4})/$', ytenx.tcenghyonhtsen.views.sieux_yonh_page, name='tcenghyonhtsen-sieux_yonh_page'),
  re_path(r'^yonhmiuk$', ytenx.tcenghyonhtsen.views.yonh_miuk_list_page, name='tcenghyonhtsen-yonh_miuk_list_page'),
  re_path(r'^yonhmiuk/(.+)/$', ytenx.tcenghyonhtsen.views.yonh_miuk_page, name='tcenghyonhtsen-yonh_miuk_page'),
  re_path(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.tcenghyonhtsen.views.cio_page, name='tcenghyonhtsen-cio_page'),
  re_path(r'^transcription_legend$', ytenx.tcenghyonhtsen.views.transcription_legend_page, name='tcenghyonhtsen-transcription_legend_page'),                                              
  re_path(r'^$', ytenx.tcenghyonhtsen.views.index_page, name='tcenghyonhtsen'),
]
