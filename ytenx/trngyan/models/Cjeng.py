# coding=utf-8
from django.db import models

#聲類
class CjengLyih(models.Model):
  mjeng = models.CharField(max_length = 2, primary_key = True)
  
  class Meta:
    app_label = 'trngyan'

  def __unicode__(self):
      return self.mjeng

#聲母
class CjengMux(models.Model):
  #代表字
  dzih = models.CharField(max_length = 1, primary_key = True)
  #聲類
  lyih = models.ForeignKey(CjengLyih, db_index = True)
  #擬音
  ngix = models.OneToOneField('NgixQim')
  
  class Meta:
    app_label = 'trngyan'

  def __unicode__(self):
    return self.dzih
