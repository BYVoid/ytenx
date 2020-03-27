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
    app_label = 'trngyan'

  def sieux_yonh(self):
    return self.sieuxyonh_set.all().order_by('ziox')
    
  def dzih(self):
    return self.dzih_set.all().order_by('ziox')
    
  def urls(self):
    base_path = '/trngyan/cio/%d/%d/'
    max_jep = {
      1: 94,
      2: 118,
    }
    urls = {
      'current': base_path % (self.kyenh, self.jep),
      'first': base_path % (self.kyenh, 1),
      'last': base_path % (self.kyenh, max_jep[self.kyenh]),
    }
    if self.jep > 1:
      urls['previous'] = base_path % (self.kyenh, self.jep - 1)
    if self.jep < max_jep[self.kyenh]:
      urls['next'] = base_path % (self.kyenh, self.jep + 1)
    return urls

#聲類
class CjengLyih(models.Model):
  mjeng = models.CharField(max_length = 2, primary_key = True)
  
  class Meta:
    app_label = 'trngyan'

  def __str__(self):
      return self.mjeng

#聲母
class CjengMux(models.Model):
  #代表字
  dzih = models.CharField(max_length = 1, primary_key = True)
  #聲類
  lyih = models.ForeignKey(CjengLyih, db_index = True, on_delete=models.DO_NOTHING)
  #擬音
  ngix = models.OneToOneField('NgixQim', on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'trngyan'

  def __str__(self):
    return self.dzih

#單字條目
class Dzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #標識符
  id = models.CharField(max_length = 2, db_index = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux_yonh = models.ForeignKey('SieuxYonh', db_index = True, on_delete=models.DO_NOTHING)
  #註釋
  tryoh = models.TextField()
  #書
  cio = models.ManyToManyField('Cio')
  
  class Meta:
    app_label = 'trngyan'
  
  def __str__(self):
    return self.dzih

#擬音
class NgixQim(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  neng_keh_piuk = models.CharField(verbose_name="寧繼福", max_length=16, null=True)
  
  class Meta:
    app_label = 'trngyan'

  def keys(self):
    return (
      'neng_keh_piuk',
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field(key).verbose_name
      value = self.__dict__[key]
      yield name, value

#小韻
class SieuxYonh(models.Model):
  #小韻序號
  ziox = models.IntegerField(primary_key = True)
  #代表字
  taj = models.CharField(max_length = 1, db_index = True)
  #聲母
  cjeng = models.ForeignKey('CjengMux', db_index = True, on_delete=models.DO_NOTHING)
  #韻部
  yonh_box = models.ForeignKey('YonhBox', db_index = True, on_delete=models.DO_NOTHING)
  #韻母
  yonh = models.ForeignKey('YonhMux', db_index = True, on_delete=models.DO_NOTHING)
  #聲調
  deuh = models.IntegerField()
  #四呼
  ho = models.IntegerField()
  #書
  cio = models.ManyToManyField('Cio')
  
  class Meta:
    app_label = 'trngyan'

  def __str__(self):
    return self.taj

  def ngix(self):
    ngix = {}
    for name,value in self.cjeng.ngix.items():
      ngix[name] = value
    for name,value in self.yonh.ngix.items():
      yield name, ngix[name] + value

#韻部
class YonhBox(models.Model):
  #名稱
  mjeng = models.CharField(max_length = 2, primary_key = True)
  
  class Meta:
    app_label = 'trngyan'
  
  def __str__(self):
    return self.mjeng
  
  def yonh_mux(self):
    yonh_mux_dzip = {}
    for yonh_mux in self.yonhmux_set.all():
      if yonh_mux.ho in yonh_mux_dzip:
        yonh_mux_dzip[yonh_mux.ho].append(yonh_mux)
      else:
        yonh_mux_dzip[yonh_mux.ho] = [yonh_mux]
    for i in range(1, 4 + 1):
      if i in yonh_mux_dzip:
        yield yonh_mux_dzip[i]
      else:
        yield []

#韻母
class YonhMux(models.Model):
  #名稱
  mjeng = models.CharField(max_length = 4, primary_key = True)
  #韻部
  yonh_box = models.ForeignKey('YonhBox', db_index = True, on_delete=models.DO_NOTHING)
  #四呼
  ho = models.IntegerField()
  #擬音
  ngix = models.OneToOneField('NgixQim', on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'trngyan'
  
  def __str__(self):
    return self.mjeng
