# coding=utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  (r'^kyonh/', include('ytenx.kyonh.urls')),
  (r'^$', 'views.index_page'),
  # Examples:
  # url(r'^$', 'ytenx.views.home', name='home'),
  # url(r'^ytenx/', include('ytenx.foo.urls')),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
  # url(r'^admin/', include(admin.site.urls)),
)
