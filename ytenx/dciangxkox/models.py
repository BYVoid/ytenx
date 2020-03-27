# coding=utf-8
from django.db import models
from ytenx.kyonh.models import SieuxYonh

#聲符
class CjengByo(models.Model):
  #代表字
  mjeng = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'dciangxkox'

  def __str__(self):
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

#韻部
class YonhBox(models.Model):
  #名稱
  mjeng = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'dciangxkox'
  
  def __str__(self):
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

#單字條目
class Dzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #標識符
  id = models.CharField(max_length = 2, db_index = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #廣韻小韻
  sieux_yonh = models.ForeignKey(SieuxYonh, related_name='+', db_index = True, null = True, on_delete=models.DO_NOTHING)
  #聲符
  cjeng = models.ForeignKey(CjengByo, db_index = True, on_delete=models.DO_NOTHING)
  #韻部
  yonh = models.ForeignKey(YonhBox, db_index = True, on_delete=models.DO_NOTHING)
  #韻部細分
  yonh_seh = models.IntegerField()
  #擬音1
  ngix_1 = models.CharField(max_length = 16)
  #擬音2
  ngix_2 = models.CharField(max_length = 16)
  #擬音3
  ngix_3 = models.CharField(max_length = 16)
  #註釋
  tryoh = models.TextField()
  
  class Meta:
    app_label = 'dciangxkox'
  
  def __str__(self):
    return self.dzih
