# coding=utf-8
from django.db import models

#聲符
class CjengByo(models.Model):
  #代表字
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

  def yonh_box(self):
    yonh_box = {}
    for dzih in self.dzih_set.all():
      yonh_box[dzih.yonh] = True
    return yonh_box.keys()
