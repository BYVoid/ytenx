# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
  (r'^kyonh/', include('ytenx.kyonh.urls')),
  (r'^$', 'views.index_page'),
)

urlpatterns += staticfiles_urlpatterns()
