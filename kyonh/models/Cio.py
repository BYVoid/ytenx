# coding=utf-8
from django.db import models

#澤存堂本
class DrakDzuonDang(models.Model):
  #卷
  kyenh = models.SmallIntegerField(db_index=True)
  #頁碼
  jep = models.SmallIntegerField(db_index=True)
  
  class Meta:
    app_label = 'kyonh'

#書
class Cio(models.Model):
  #澤存堂本
  drakDzuonDang = models.ForeignKey(DrakDzuonDang)
  
  class Meta:
    app_label = 'kyonh'
