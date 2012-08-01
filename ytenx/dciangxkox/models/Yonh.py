# coding=utf-8
from django.db import models

#韻部
class YonhBox(models.Model):
  #名稱
  mjeng = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'dciangxkox'
  
  def __unicode__(self):
    return self.mjeng

  def ngix(self):
    ngix = {}
    for dzih in self.dzih_set.all():
      ngix[dzih.ngix_1] = True
    return ngix.keys()

  def cjeng_byo(self):
    cjeng_byo = {}
    for dzih in self.dzih_set.all():
      cjeng_byo[dzih.cjeng] = True
    return cjeng_byo.keys()
