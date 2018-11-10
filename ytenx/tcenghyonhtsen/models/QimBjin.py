# coding=utf-8
from django.db import models

#小韻
class QimBjin(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #平聲小韻號
  t1 = models.IntegerField(db_index = True)
  #上聲小韻號
  t2 = models.IntegerField(db_index = True)
  #去聲小韻號
  t3 = models.IntegerField(db_index = True)
  #入聲小韻號
  t4 = models.IntegerField(db_index = True)
  #重上聲是否歸于去聲
  merge_t2_t3 = models.BooleanField();
  #文件名
  filename = models.CharField(max_length = 16, db_index = True);
  
  class Meta:
    app_label = 'tcenghyonhtsen'
