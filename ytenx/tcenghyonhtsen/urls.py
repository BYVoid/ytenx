# coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
  (r'^sync$', 'ytenx.tcenghyonhtsen.sync.sync'),
  (r'^$', 'ytenx.tcenghyonhtsen.views.index_page'),
)
