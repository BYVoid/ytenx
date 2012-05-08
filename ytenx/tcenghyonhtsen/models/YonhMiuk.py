# coding=utf-8
from django.db import models

#韻目
class YonhMiuk(models.Model):
  #代表字
  dzih = models.CharField(max_length = 2, primary_key = True)
  #韻部
  bux = models.ForeignKey('YonhBux', db_index = True)
  #調
  deuh = models.SmallIntegerField()
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih
