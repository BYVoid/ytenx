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

  def sieux_yonh(self):
    return self.sieuxyonh_set.all().order_by('ziox')
    
  def dzih(self):
    return self.dzih_set.all().order_by('ziox')
    
  def urls(self):
    base_path = '/pyonh/cio/%d/%d/'
    max_jep = {
      1: 105,
      2: 97,
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
