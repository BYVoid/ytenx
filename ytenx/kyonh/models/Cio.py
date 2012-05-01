# coding=utf-8
from django.db import models

#澤存堂本
class DrakDzuonDang(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=4)
  #卷
  kyenh = models.SmallIntegerField(db_index=True)
  #頁碼
  jep = models.SmallIntegerField(db_index=True)
  
  class Meta:
    app_label = 'kyonh'
  
  def __unicode__(self):
    return '%03d' % self.jep

#書
class Cio(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=4)
  #澤存堂本
  drakDzuonDang = models.OneToOneField(DrakDzuonDang)
  
  class Meta:
    app_label = 'kyonh'
