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
  
  def yonh_mux(self):
    yonh_mux_dzip = {}
    for yonh_mux in self.yonhmux_set.all():
      if yonh_mux_dzip.has_key(yonh_mux.ho):
        yonh_mux_dzip[yonh_mux.ho].append(yonh_mux)
      else:
        yonh_mux_dzip[yonh_mux.ho] = [yonh_mux]
    for i in range(1, 4 + 1):
      if yonh_mux_dzip.has_key(i):
        yield yonh_mux_dzip[i]
      else:
        yield []

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
