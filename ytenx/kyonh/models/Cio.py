# coding=utf-8
from django.db import models

#澤存堂本
class DrakDzuonDang(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=4)
  #卷
  kyenh = models.SmallIntegerField(db_index=True)
  #頁碼
  jep = models.SmallIntegerField(db_index=True)
  
  class Meta:
    app_label = 'kyonh'
  
  def __unicode__(self):
    return '%03d' % self.jep
  
  def urls(self):
    base_path = '/kyonh/cio/%d/%d/'
    max_jep = {
      1: 72,
      2: 56,
      3: 58,
      4: 60,
      5: 59,
    }
    urls = {
      'current': base_path % (self.kyenh, self.jep),
      'first': base_path % (self.kyenh, 1),
      'last': base_path % (self.kyenh, max_jep[self.kyenh]),
    }
    if self.jep > 1:
      urls['previous'] = base_path % (self.kyenh, self.jep - 1)
    elif self.kyenh > 1:
      urls['previous'] = base_path % (self.kyenh - 1, max_jep[self.kyenh - 1])
    if self.jep < max_jep[self.kyenh]:
      urls['next'] = base_path % (self.kyenh, self.jep + 1)
    elif self.kyenh < 5:
      urls['next'] = base_path % (self.kyenh + 1, 1)
    
    return urls

#書
class Cio(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=4)
  #澤存堂本
  drakDzuonDang = models.OneToOneField(DrakDzuonDang)
  
  class Meta:
    app_label = 'kyonh'
