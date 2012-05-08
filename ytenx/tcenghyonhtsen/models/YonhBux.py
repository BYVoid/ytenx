# coding=utf-8
from django.db import models

#韻部
class YonhBux(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #代表字
  dzih = models.CharField(max_length = 2, unique = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih;
  
  def miuk(self):
    dzip = {}
    for yonh in self.yonhmiuk_set.all():
      if yonh.deuh == 1:
        dzip['bieng'] = yonh
      elif yonh.deuh == 2:
        dzip['dciangx'] = yonh
      elif yonh.deuh == 3:
        dzip['khioh'] = yonh
      elif yonh.deuh == 4:
        dzip['njip'] = yonh
    return dzip
