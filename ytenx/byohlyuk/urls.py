# coding=utf-8
from django.urls import re_path
from ytenx.byohlyuk.views import byoh_lyuk

urlpatterns = [
  re_path(r'^(.*)', byoh_lyuk, name='byoh_lyuk'),
]
