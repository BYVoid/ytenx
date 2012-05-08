# coding=utf-8
from django.db import models

#韻部
class YonhBux(models.Model):
  #代表字
  dzih = models.CharField(max_length = 2, primary_key = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih;
  
  def dzip(self):
    dzip = {}
    for yonh in self.bux_set:
      if yonh.deuh == 1:
        dzip['bieng'] = yonh
      elif yonh.deuh == 2:
        dzip['dciangx'] = yonh
      elif yonh.deuh == 3:
        dzip['khioh'] = yonh
      elif yonh.deuh == 4:
        dzip['njip'] = yonh
    return dzip
