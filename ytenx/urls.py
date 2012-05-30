# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
  (r'^kyonh/', include('ytenx.kyonh.urls')),
  (r'^tcyts/', include('ytenx.tcenghyonhtsen.urls')),
  (r'^$', 'ytenx.views.index_page'),
  (r'^about$', 'ytenx.views.about_page'),
  (r'^zim$', 'ytenx.views.zim'),
)

urlpatterns += staticfiles_urlpatterns()
