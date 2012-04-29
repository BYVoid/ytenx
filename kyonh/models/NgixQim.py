# coding=utf-8
from django.db import models

#擬音
class NgixQim(models.Model):
  kauPuonxHanh = models.CharField(verbose_name="高本漢", max_length=16)
  lixPyangKueh = models.CharField(verbose_name="李方桂", max_length=16)
  yangLik = models.CharField(verbose_name="王力", max_length=16)
  tciuPyapKau = models.CharField(verbose_name="周法高", max_length=16)
  liukTcihYoi = models.CharField(verbose_name="陸志韋", max_length=16)
  tungxDungGhua = models.CharField(verbose_name="董同龢", max_length=16)
  lixYeng = models.CharField(verbose_name="李榮", max_length=16)
  dcjeuhYengPhyon = models.CharField(verbose_name="邵榮芬", max_length=16)
  drienghTriangDciangPyang = models.CharField(verbose_name="鄭張尚方", max_length=16)
  phuanNgohYon = models.CharField(verbose_name="潘悟雲", max_length=16)
  boLipPuonx = models.CharField(verbose_name="蒲立本", max_length=16)
  
  class Meta:
    app_label = 'kyonh'

