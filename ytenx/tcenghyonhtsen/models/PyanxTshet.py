# coding=utf-8
from django.db import models
from SieuxYonh import SieuxYonh

#反切上字
class DciangxDzih(models.Model):
  dzih = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return unicode(self.dzih)
  
  #反切
  def pyanx(self):
    return PyanxTshet.objects.filter(dciangx=self)
  
  #小韻
  def sieuxYonh(self):
    return SieuxYonh.objects.filter(pyanx__in=self.pyanx())

#反切下字
class GhraxDzih(models.Model):
  dzih = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return unicode(self.dzih)
  
  #反切
  def pyanx(self):
    return PyanxTshet.objects.filter(ghrax=self)
  
  #小韻
  def sieuxYonh(self):
    return SieuxYonh.objects.filter(pyanx__in=self.pyanx())

#反切
class PyanxTshet(models.Model):
  #反切
  tshet = models.CharField(max_length = 2, primary_key = True)
  #反切上字
  dciangx = models.ForeignKey(DciangxDzih, db_index = True)
  #反切下字
  ghrax = models.ForeignKey(GhraxDzih, db_index = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dciangx.dzih + self.ghrax.dzih
