# coding=utf-8
from django.db import models

#擬音
class NgixQim(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  triang_gyon_henx = models.CharField(verbose_name="張羣顯", max_length=16, null=True)
  
  class Meta:
    app_label = 'pyonh'

  def keys(self):
    return (
      'triang_gyon_henx',
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field_by_name(key)[0].verbose_name
      value = self.__dict__[key]
      yield name, value
