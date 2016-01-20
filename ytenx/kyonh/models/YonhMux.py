# coding=utf-8
from django.db import models
from SieuxYonh import SieuxYonh

class YonhMuxManager(models.Manager):
  #獲取舒入配合表
  def get_pairs(self):
    yonh_mux_list = []
    traversed = {}
    
    for yonh in self.all():
      if traversed.has_key(yonh.mjeng): continue
      traversed[yonh.mjeng] = True
      item = {
        'gheh': yonh.gheh,
        'tongx': yonh.tongx,
        'ho': yonh.ho,
        'cio': None,
        'tshyuk': None,
      }
  
      tuaih = ''
      if yonh.tuaih:
        tuaih = yonh.tuaih
        traversed[yonh.tuaih.mjeng] = True
      
      if not yonh.tshyuk:
        item['cio'] = yonh
        item['tshyuk'] = tuaih
      else:
        item['tshyuk'] = yonh
        item['cio'] = tuaih
      
      yonh_mux_list.append(item)
    
    return yonh_mux_list

#韻母
class YonhMux(models.Model):
  #韻母名稱
  mjeng = models.CharField(max_length=3, primary_key = True)
  #所屬韻系
  gheh = models.ForeignKey('YonhGheh', db_index=True)
  #等
  tongx = models.SmallIntegerField(db_index=True)
  #開合口呼
  ho = models.BooleanField(db_index=True, default=False)
  #促舒
  tshyuk = models.BooleanField(db_index=True, default=False)
  #同位對立入聲/舒聲
  tuaih = models.OneToOneField('YonhMux', null=True)
  #擬音
  ngix = models.OneToOneField('NgixQim')
  #拼音
  preng = models.OneToOneField('PrengQim')
  
  objects = YonhMuxManager()
  
  class Meta:
    app_label = 'kyonh'
  
  def __unicode__(self):
      return self.mjeng

  #小韻
  def sieuxYonh(self):
    return SieuxYonh.objects.filter(yonh=self)
