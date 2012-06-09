# coding=utf-8
from django.db import models

#書葉
class Cio(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=5)
  #卷
  kyenh = models.SmallIntegerField(db_index=True)
  #頁碼
  jep = models.SmallIntegerField(db_index=True)
  
  class Meta:
    app_label = 'pyonh'
