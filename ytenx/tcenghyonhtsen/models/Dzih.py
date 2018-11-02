# coding=utf-8
from django.db import models
import ytenx.kyonh.models

#單字條目
class Dzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True)
  #書頁
  cio = models.ManyToManyField('Cio')
  #字義
  ngieh = models.TextField();
  #對應廣韻小韻
  kwangx = models.ForeignKey(ytenx.kyonh.models.SieuxYonh, related_name='tcengh', null = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih

#古音
class KoxQim(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True)
  #書頁
  cio = models.ManyToManyField('Cio');
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih

#逸字
class JitDzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True)
  #書頁
  cio = models.ManyToManyField('Cio');
  #字義
  ngieh = models.TextField();
  #對應廣韻小韻
  kwangx = models.ForeignKey(ytenx.kyonh.models.SieuxYonh, related_name='tcengh_jit', null = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih
