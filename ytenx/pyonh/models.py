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
    if self.jep < max_jep[self.kyenh]:
      urls['next'] = base_path % (self.kyenh, self.jep + 1)
    return urls

#聲類
class CjengLyih(models.Model):
  mjeng = models.CharField(max_length = 5, primary_key = True)
  
  class Meta:
    app_label = 'pyonh'

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
    app_label = 'pyonh'

  def __str__(self):
    return self.dzih

#單字條目
class Dzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux_yonh = models.ForeignKey('SieuxYonh', db_index = True, on_delete=models.DO_NOTHING)
  #字義
  ngieh = models.TextField()
  #書
  cio = models.ManyToManyField('Cio')
  
  class Meta:
    app_label = 'pyonh'
  
  def __str__(self):
      return self.dzih

#擬音
class NgixQim(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  triang_gyon_henx = models.CharField(verbose_name="張羣顯", max_length=16, null=True)
  
  class Meta:
    app_label = 'pyonh'

  def keys(self):
    return (
      'triang_gyon_henx',
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field(key).verbose_name
      value = self.__dict__[key]
      yield name, value

#韻部
class YonhBox(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #名稱
  mjeng = models.CharField(max_length = 4, db_index = True, unique = True)
  
  class Meta:
    app_label = 'pyonh'
  
  def __str__(self):
    return self.mjeng

#韻母
class YonhMux(models.Model):
  #字
  mjeng = models.CharField(max_length = 3, primary_key = True)
  #韻部
  yonh_box = models.ForeignKey('YonhBox', db_index = True, on_delete=models.DO_NOTHING)
  #促舒
  tshyuk = models.BooleanField(default=False)
  #對立韻母
  tuaih = models.ForeignKey('YonhMux', null = True, on_delete=models.DO_NOTHING)
  #擬音
  ngix = models.OneToOneField('NgixQim', on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'pyonh'
  
  def __str__(self):
    return self.mjeng

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
  #陰陽
  qim_jang = models.BooleanField(default=False)
  #聲調
  deuh = models.IntegerField()
  #書
  cio = models.ManyToManyField('Cio')
  
  class Meta:
    app_label = 'pyonh'

  def __str__(self):
    return self.taj
