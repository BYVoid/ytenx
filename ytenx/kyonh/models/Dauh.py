# coding=utf-8
from django.db import models

#拼音
class Dauh(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  putonghua = models.CharField(verbose_name="推導普通話", max_length=12, null=True)
  tcengh = models.CharField(verbose_name="推導中州音", max_length=30, null=True)
  
  class Meta:
    app_label = 'kyonh'

  def keys(self):
    return (
      'putonghua',
      'tcengh', 
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field_by_name(key)[0].verbose_name
      value = self.__dict__[key]
      yield name, value
