# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = patterns('',
  (r'^kyonh/', include('ytenx.kyonh.urls')),
  (r'^tcyts/', include('ytenx.tcenghyonhtsen.urls')),
  (r'^pyonh/', include('ytenx.pyonh.urls')),
  (r'^$', 'ytenx.views.index_page'),
  (r'^about$', 'ytenx.views.about_page'),
  (r'^zim$', 'ytenx.views.zim'),
  (r'^sriek$', 'ytenx.views.kiemx_sriek'),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
  urlpatterns += patterns('',
    (r'^sync/jitthex$', 'ytenx.sync.jihthex.sync'),
  )
