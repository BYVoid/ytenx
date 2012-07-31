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
