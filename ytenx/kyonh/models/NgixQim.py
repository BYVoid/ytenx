# coding=utf-8
from django.db import models

#擬音
class NgixQim(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  kauPuonxHanh = models.CharField(verbose_name="高本漢", max_length=16, null=True)
  lixPyangKueh = models.CharField(verbose_name="李方桂", max_length=16, null=True)
  yangLik = models.CharField(verbose_name="王力", max_length=16, null=True)
  tciuPyapKau = models.CharField(verbose_name="周法高", max_length=16, null=True)
  liukTcihYoi = models.CharField(verbose_name="陸志韋", max_length=16, null=True)
  tungxDungGhua = models.CharField(verbose_name="董同龢", max_length=16, null=True)
  lixYeng = models.CharField(verbose_name="李榮", max_length=16, null=True)
  dcjeuhYengPhyon = models.CharField(verbose_name="邵榮芬", max_length=16, null=True)
  drienghTriangDciangPyang = models.CharField(verbose_name="鄭張尚芳", max_length=16, null=True)
  phuanNgohYon = models.CharField(verbose_name="潘悟雲", max_length=16, null=True)
  boLipPuonx = models.CharField(verbose_name="蒲立本", max_length=16, null=True)
  
  class Meta:
    app_label = 'kyonh'

  def keys(self):
    return (
      'kauPuonxHanh',
      'lixPyangKueh', 
      'yangLik',
      'tciuPyapKau',
      'liukTcihYoi',
      'tungxDungGhua',
      'lixYeng',
      'dcjeuhYengPhyon',
      'drienghTriangDciangPyang',
      'phuanNgohYon', 
      'boLipPuonx',
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field_by_name(key)[0].verbose_name
      value = self.__dict__[key]
      yield name, value
