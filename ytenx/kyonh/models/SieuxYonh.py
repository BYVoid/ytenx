# coding=utf-8
from django.db import models
from Dzih import Dzih

class DeuhGhang:
  def __init__(self, miuk):
    self.miuk = miuk
    self.ho_ghang = []

class SieuxYonhManager(models.Manager):
  def get_yonh_do(self, dzip):
    from CjengMux import CjengMux
    from YonhMux import YonhMux
    
    cjeng_mux = CjengMux.objects.all()

    yonh_do = []
    #分四聲
    for deuh in range(1, 5):
      miuk = dzip.get_by_deuh(deuh)
      deuh_ghang = DeuhGhang(miuk)
      yonh_do.append(deuh_ghang)
      #分開合
      for ho in (True, False):
        deuh_ghang.ho_ghang.append([])
        ho_key = 1 - int(ho)
        #分四等
        for tongx in range(1, 5):
          tongx_key = tongx - 1
          deuh_ghang.ho_ghang[ho_key].append([])
          yonh = YonhMux.objects.filter(
            gheh = dzip.gheh(),
            ho = ho,
            tongx = tongx,
            tshyuk = (deuh == 4),
          )
          if not yonh:
            yonh = None
          else:
            assert(len(yonh) == 1)
            yonh = yonh[0]
          #分聲母
          sieux_ghang = []
          for cjeng in cjeng_mux:
            if not yonh:
              sieux_ghang.append(None)
              continue
            sieux = self.filter(
              cjeng = cjeng,
              yonh = yonh,
              yonhMiuk = miuk,
            )
            if not sieux:
              sieux = None
            else:
              #assert(len(sieux) == 1)
              sieux = sieux[0]
            sieux_ghang.append(sieux)
          deuh_ghang.ho_ghang[ho_key][tongx_key] = sieux_ghang
    return yonh_do

#小韻
class SieuxYonh(models.Model):
  #小韻序號
  ziox = models.IntegerField(primary_key = True)
  #代表字
  taj = models.CharField(max_length = 1, db_index=True)
  #聲母
  cjeng = models.ForeignKey('CjengMux', db_index = True)
  #韻母
  yonh = models.ForeignKey('YonhMux', db_index = True)
  #韻目
  yonhMiuk = models.ForeignKey('YonhMiuk', db_index = True)
  #反切
  pyanx = models.ForeignKey('PyanxTshet', db_index = True, null = True)
  #擬音
  ngix = models.OneToOneField('NgixQim')
  #拼音
  preng = models.OneToOneField('PrengQim')
  #書
  cio = models.ManyToManyField('Cio')
  
  objects = SieuxYonhManager()
  
  class Meta:
    app_label = 'kyonh'

  def __unicode__(self):
    return self.taj

  #字
  def dzih(self):
    return Dzih.objects.filter(sieuxYonh = self)
  
  #聲調
  def deuh(self):
    return self.yonhMiuk.deuh
