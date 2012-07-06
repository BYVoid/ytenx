# coding=utf-8
from django.db import models

#韻部
class YonhBox(models.Model):
  #名稱
  mjeng = models.CharField(max_length = 2, primary_key = True)
  
  class Meta:
    app_label = 'trngyan'
  
  def __unicode__(self):
    return self.mjeng

#韻母
class YonhMux(models.Model):
  #名稱
  mjeng = models.CharField(max_length = 4, primary_key = True)
  #韻部
  yonh_box = models.ForeignKey('YonhBox', db_index = True)
  #四呼
  ho = models.IntegerField()
  #擬音
  ngix = models.OneToOneField('NgixQim')
  
  class Meta:
    app_label = 'trngyan'
  
  def __unicode__(self):
    return self.mjeng
