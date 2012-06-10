# coding=utf-8
from django.db import models

#韻部
class YonhBox(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #名稱
  mjeng = models.CharField(max_length = 4, db_index = True, unique = True)
  
  class Meta:
    app_label = 'pyonh'
  
  def __unicode__(self):
    return self.mjeng

#韻母
class YonhMux(models.Model):
  #字
  mjeng = models.CharField(max_length = 3, primary_key = True)
  #韻部
  yonh_box = models.ForeignKey('YonhBox', db_index = True)
  #促舒
  tshyuk = models.BooleanField()
  #對立韻母
  tuaih = models.ForeignKey('YonhMux', null = True)
  #擬音
  ngix = models.OneToOneField('NgixQim')
  
  class Meta:
    app_label = 'pyonh'
  
  def __unicode__(self):
    return self.mjeng
