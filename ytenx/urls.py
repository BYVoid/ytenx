# coding=utf-8
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ytenx.views import index_page, renew_session, about_page, zim, kiemx_sriek

urlpatterns = [
  url(r'^kyonh/', include('ytenx.kyonh.urls')),
  url(r'^tcyts/', include('ytenx.tcenghyonhtsen.urls')),
  url(r'^pyonh/', include('ytenx.pyonh.urls')),
  url(r'^trngyan/', include('ytenx.trngyan.urls')),
  url(r'^dciangx/', include('ytenx.dciangxkox.urls')),
  url(r'^byohlyuk/', include('ytenx.byohlyuk.urls')),
  url(r'^$', index_page, name='index_page'),
  url(r'^r$', renew_session, name='renew_session'),
  url(r'^about$', about_page, name='about_page'),
  url(r'^zim$', zim, name='zim'),
  url(r'^sriek$', kiemx_sriek, name='kiemx_sriek'),
]

urlpatterns += staticfiles_urlpatterns()
