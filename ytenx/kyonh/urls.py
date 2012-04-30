# coding=utf-8
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^sync$', 'ytenx.kyonh.sync.sync'),
)
