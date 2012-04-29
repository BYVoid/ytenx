# coding=utf-8
from django.db import models
from Dzih import Dzih

#小韻
class SieuxYonh(models.Model):
  #小韻序號
  ziox = models.IntegerField(primary_key = True)
  #聲母
  cjeng = models.ForeignKey('CjengMux', db_index = True)
  #韻母
  yonh = models.ForeignKey('YonhMux', db_index = True)
  #韻目
  yonhMiuk = models.ForeignKey('YonhMiuk', db_index = True)
  #反切
  pyanx = models.ForeignKey('PyanxTshet', null = True, db_index = True)
  #擬音
  ngix = models.ForeignKey('NgixQim')
  #拼音
  preng = models.ForeignKey('PrengQim')
  #書
  cio = models.ManyToManyField('Cio')
  
  class Meta:
    app_label = 'kyonh'

  #字
  def dzih(self):
    return Dzih.objects.filter(sieuxYonh = self)
  
  #聲調
  def deuh(self):
    return self.yonhMiuk.deuh
