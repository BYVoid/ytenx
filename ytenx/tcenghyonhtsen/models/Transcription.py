# coding=utf-8
from django.db import models
import ytenx.kyonh.models

#韻母轉寫
class GhiunhTranscription(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #韻部
  ghiunhBox = models.CharField(max_length = 4)
  #譯訓舒聲
  shioJiekHiunh = models.CharField(max_length = 8)
  #舒聲IPA轉寫
  shioIpa = models.CharField(max_length = 16)
  #譯訓舒聲
  njipJiekHiunh = models.CharField(max_length = 8)
  #舒聲IPA轉寫
  njipIpa = models.CharField(max_length = 16)

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.shioIpa

#聲母轉寫
class ShiengTranscription(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #聲類
  shiengLwih = models.CharField(max_length = 4)
  #譯訓
  jiekHiunh = models.CharField(max_length = 8)
  #IPA轉寫
  ipa = models.CharField(max_length = 16)
  #備註
  memo = models.TextField();

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.ipa

#聲調轉寫
class DewhTranscription(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #調類
  dewhLwih = models.CharField(max_length = 4)
  #譯訓
  jiekHiunh = models.CharField(max_length = 8)
  #IPA轉寫
  ipa = models.CharField(max_length = 16)
  #備註
  memo = models.TextField();

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.ipa
