# coding=utf-8
import ytenx
from django.conf.urls import url
from ytenx.tcenghyonhtsen.views import *

urlpatterns = [
  url(r'^sieux$', ytenx.tcenghyonhtsen.views.sieux_yonh_list_page, name='tcenghyonhtsen-sieux_yonh_list_page'),
  url(r'^sieux/(\d{1,4})/$', ytenx.tcenghyonhtsen.views.sieux_yonh_page, name='tcenghyonhtsen-sieux_yonh_page'),
  url(r'^yonhmiuk$', ytenx.tcenghyonhtsen.views.yonh_miuk_list_page, name='tcenghyonhtsen-yonh_miuk_list_page'),
  url(r'^yonhmiuk/(.+)/$', ytenx.tcenghyonhtsen.views.yonh_miuk_page, name='tcenghyonhtsen-yonh_miuk_page'),
  url(r'^cio/(\d{1,1})/(\d{1,3})/$', ytenx.tcenghyonhtsen.views.cio_page, name='tcenghyonhtsen-cio_page'),
  url(r'^transcription_legend$', ytenx.tcenghyonhtsen.views.transcription_legend_page, name='tcenghyonhtsen-transcription_legend_page'),                                              
  url(r'^$', ytenx.tcenghyonhtsen.views.index_page, name='tcenghyonhtsen'),
]
