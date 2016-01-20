# coding=utf-8
from django.conf.urls import patterns
from django.conf import settings

urlpatterns = patterns('',
  (r'^(.*)', 'ytenx.byohlyuk.views.byoh_lyuk'),
)
