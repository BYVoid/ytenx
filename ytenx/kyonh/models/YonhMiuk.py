# coding=utf-8
from django.db import models
from YonhMux import YonhMux
from SieuxYonh import SieuxYonh

#廣韻目次
class KuangxYonhMiukTshiih(models.Model):
  #代表字
  dzih = models.CharField(max_length = 1, unique = True)
  #卷 上平 下平 上 去 入
  kyenh = models.CharField(max_length = 2)
  #廣韻韻目序號
  tshiih = models.SmallIntegerField()
  
  class Meta:
    app_label = 'kyonh'
  
  def __unicode__(self):
      return self.kyenh + self.tshiih + self.dzih;

#韻目
class YonhMiuk(models.Model):
  #代表字
  dzih = models.CharField(max_length = 1, unique = True)
  #所屬韻系
  gheh = models.ForeignKey('YonhGheh', db_index=True)
  #調
  deuh = models.SmallIntegerField()
  #廣韻目次
  tshiih = models.ForeignKey(KuangxYonhMiukTshiih)
  #韻母
  yonh = models.ManyToManyField('YonhMux')
  
  class Meta:
    app_label = 'kyonh'
  
  def __unicode__(self):
      return self.character
  
  #小韻
  def sieuxYonh(self):
      return SieuxYonh.objects.filter(yonh=self)
