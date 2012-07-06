# coding=utf-8
from django.db import models

#單字條目
class Dzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #標識符
  id = models.CharField(max_length = 2, db_index = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux_yonh = models.ForeignKey('SieuxYonh', db_index = True)
  #註釋
  tryoh = models.TextField()
  #書
  cio = models.ManyToManyField('Cio')
  
  class Meta:
    app_label = 'trngyan'
  
  def __unicode__(self):
    return self.dzih
