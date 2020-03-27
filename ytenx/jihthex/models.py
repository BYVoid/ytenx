# coding=utf-8
from django.db import models

#書葉
class Dzih(models.Model):
  #字
  dzih = models.CharField(primary_key=True, max_length=1)
  #全等異體
  dzyen_tongx = models.ManyToManyField('Dzih', related_name='dzyen_tongx_pyanx')
  #語義交疊異體
  krau_dep = models.ManyToManyField('Dzih', related_name='krau_dep_pyanx')
  #簡體
  krenx = models.ManyToManyField('Dzih', related_name='krenx_pyanx')
  #繁體
  byan = models.ManyToManyField('Dzih', related_name='byan_pyanx')
  #Unihan所未收錄者
  tha = models.ManyToManyField('Dzih', related_name='tha_pyanx')

  def __str__(self):
    return self.dzih
