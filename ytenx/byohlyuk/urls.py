# coding=utf-8
from django.conf.urls import url
from ytenx.byohlyuk.views import byoh_lyuk

urlpatterns = [
  url(r'^(.*)', byoh_lyuk, name='byoh_lyuk'),
]
