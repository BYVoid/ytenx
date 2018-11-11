# coding=utf-8
from django.db import models

#小韻
class QimBjin(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #平聲小韻號
  t1 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_1', db_index = True, null = True)
  #上聲小韻號
  t2 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_2', db_index = True, null = True)
  #去聲小韻號
  t3 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_3', db_index = True, null = True)
  #入聲小韻號
  t4 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_4', db_index = True, null = True)
  #重上聲是否歸于去聲
  merge_t2_t3 = models.BooleanField();
  #是否可有入聲
  has_t4 = models.BooleanField();
  #文件名
  filename = models.CharField(max_length = 16, db_index = True);
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    def getIPA(sieuxYonh):
      if sieuxYonh == None:
        return u'?'
      return sieuxYonh.ipa
    
    text = u'平' + getIPA(self.t1)
    if self.merge_t2_t3:
      text = text + u' 上去'
      if getIPA(self.t3) != '?':
        text = text + getIPA(self.t3)
      else:
        text = text + getIPA(self.t2)
    else:
      text = text + u' 上' + getIPA(self.t2) + u' 去' + getIPA(self.t3)
    if self.has_t4:
      text = text + u' 入' + getIPA(self.t4)
    return text
