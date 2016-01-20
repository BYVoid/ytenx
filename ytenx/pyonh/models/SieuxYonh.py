# coding=utf-8
from django.db import models

#小韻
class SieuxYonh(models.Model):
  #小韻序號
  ziox = models.IntegerField(primary_key = True)
  #代表字
  taj = models.CharField(max_length = 1, db_index = True)
  #聲母
  cjeng = models.ForeignKey('CjengMux', db_index = True)
  #韻部
  yonh_box = models.ForeignKey('YonhBox', db_index = True)
  #韻母
  yonh = models.ForeignKey('YonhMux', db_index = True)
  #陰陽
  qim_jang = models.BooleanField(default=False)
  #聲調
  deuh = models.IntegerField()
  #書
  cio = models.ManyToManyField('Cio')
  
  class Meta:
    app_label = 'pyonh'

  def __unicode__(self):
    return self.taj
