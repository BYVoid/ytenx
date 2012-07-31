# coding=utf-8
from django.db import models

#聲符
class CjengByo(models.Model):
  #代表字
  mjeng = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'dciangxkox'

  def __unicode__(self):
    return self.dzih
