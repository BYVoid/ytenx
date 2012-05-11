# coding=utf-8
from django.db import models
from ytenx.filters.templatetags.ytenx import sryoh

#韻目
class YonhMiuk(models.Model):
  #序號
  ziox = models.IntegerField()
  #代表字
  dzih = models.CharField(max_length = 2, primary_key = True)
  #韻部
  bux = models.ForeignKey('YonhBux', db_index = True)
  #調
  deuh = models.SmallIntegerField()
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return sryoh(self.ziox) + self.dzih

  def cio(self):
    def cmp(x, y):
      if x.kyenh < y.kyenh:
        return -1
      elif x.kyenh > y.kyenh:
        return 1
      if x.jep < y.jep:
        return -1
      else:
        return 1
  
    cio_map = {}
    for sieux in self.sieuxyonh_set.all():
      for cio in sieux.cio.all():
        cio_map[cio.identifier] = cio
    cio = cio_map.values()
    cio.sort(cmp)
    return cio