# coding=utf-8
from django.db import models

#單字條目
class Dzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index=True)
  #小韻
  sieuxYonh = models.ForeignKey('SieuxYonh', db_index=True)
  #小韻中位置
  yih = models.IntegerField(db_index=True)
  #字義
  ngieh = models.TextField()
  
  class Meta:
    app_label = 'kyonh'
  
  def __unicode__(self):
      return self.dzih
