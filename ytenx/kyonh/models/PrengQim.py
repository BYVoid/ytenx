# coding=utf-8
from django.db import models

#拼音
class PrengQim(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  polyhedron = models.CharField(verbose_name="古韻羅馬字", max_length=12, null=True)
  hiovNivv = models.CharField(verbose_name="有女羅馬字", max_length=12, null=True)
  baxter = models.CharField(verbose_name="Baxter transcription", max_length=12, null=True)
  tcengh = models.CharField(verbose_name="Baxter transcription", max_length=30, null=True)  
  putonghua = models.CharField(verbose_name="Baxter transcription", max_length=12, null=True)
  
  class Meta:
    app_label = 'kyonh'

  def keys(self):
    return (
      'polyhedron', 
      'hiovNivv',
      'baxter',
      'tcengh',
      'putonghua',
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field_by_name(key)[0].verbose_name
      value = self.__dict__[key]
      yield name, value
