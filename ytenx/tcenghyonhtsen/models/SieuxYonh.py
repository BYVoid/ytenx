# coding=utf-8
from django.db import models

#小韻
class SieuxYonh(models.Model):
  #小韻序號
  ziox = models.IntegerField(primary_key = True)
  #代表字
  taj = models.CharField(max_length = 1, db_index = True)
  #韻目
  yonhMiuk = models.ForeignKey('YonhMiuk', db_index = True)
  #反切
  pyanx = models.ForeignKey('PyanxTshet', db_index = True, null = True)
  #書頁
  cio = models.ManyToManyField('Cio')
  #IPA
  ipa = models.CharField(max_length = 16, db_index = True);
  
  class Meta:
    app_label = 'tcenghyonhtsen'

  def __unicode__(self):
    return self.taj
  
  #聲調
  def deuh(self):
    return self.yonhMiuk.deuh

  def ziox_cio(self):
    return self.cio.order_by('kyenh').order_by('jep').all()
