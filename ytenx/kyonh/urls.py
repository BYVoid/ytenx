# coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
  (r'^sync$', 'ytenx.kyonh.sync.sync'),
  (r'^intro$', 'ytenx.kyonh.views.intro_page'),
  (r'^$', 'ytenx.kyonh.views.index_page'),
)
