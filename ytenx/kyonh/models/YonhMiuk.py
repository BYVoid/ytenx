# coding=utf-8
from django.db import models
from YonhMux import YonhMux
from SieuxYonh import SieuxYonh

#廣韻目次
class KuangxYonhMiukTshiih(models.Model):
  #代表字
  dzih = models.CharField(max_length = 1, primary_key = True)
  #卷 上平 下平 上 去 入
  kyenh = models.CharField(max_length = 2)
  #廣韻韻目序號
  tshiih = models.SmallIntegerField()
  
  class Meta:
    app_label = 'kyonh'
  
  def __unicode__(self):
    from ytenx.filters.templatetags.ytenx import sryoh
    return self.kyenh + sryoh(unicode(self.tshiih)) + self.dzih;

#韻目
class YonhMiuk(models.Model):
  #代表字
  dzih = models.CharField(max_length = 2, primary_key = True)
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
    return self.dzih

#韻目集合
class YonhMiukDzip(models.Model):
  #平
  bieng = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+')
  #上
  dciangx = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+')
  #去
  khioh = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+')
  #入
  njip = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+')

  class Meta:
    app_label = 'kyonh'

  #韻系
  def gheh(self):
    if self.bieng: return self.bieng.gheh
    if self.dciangx: return self.dciangx.gheh
    if self.khioh: return self.khioh.gheh
    return self.njip.gheh

  #根據聲調獲取韻目
  def get_by_deuh(self, deuh):
    assert(deuh >=1 and deuh <= 4)
    if deuh == 1: return self.bieng
    if deuh == 2: return self.dciangx
    if deuh == 3: return self.khioh
    return self.njip
