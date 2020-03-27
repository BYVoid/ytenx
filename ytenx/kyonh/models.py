# coding=utf-8
from django.db import models

class YonhMuxManager(models.Manager):
  #獲取舒入配合表
  def get_pairs(self):
    yonh_mux_list = []
    traversed = {}
    
    for yonh in self.all():
      if yonh.mjeng in traversed: continue
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
  gheh = models.ForeignKey('YonhGheh', db_index=True, on_delete=models.DO_NOTHING)
  #等
  tongx = models.SmallIntegerField(db_index=True)
  #開合口呼
  ho = models.BooleanField(db_index=True, default=False)
  #促舒
  tshyuk = models.BooleanField(db_index=True, default=False)
  #同位對立入聲/舒聲
  tuaih = models.OneToOneField('YonhMux', null=True, on_delete=models.DO_NOTHING)
  #擬音
  ngix = models.OneToOneField('NgixQim', on_delete=models.DO_NOTHING)
  #拼音
  preng = models.OneToOneField('PrengQim', on_delete=models.DO_NOTHING)
  
  objects = YonhMuxManager()
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
      return self.mjeng

  #小韻
  def sieuxYonh(self):
    return SieuxYonh.objects.filter(yonh=self)

#拼音
class PrengQim(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  polyhedron = models.CharField(verbose_name="古韻羅馬字", max_length=12, null=True)
  hiovNivv = models.CharField(verbose_name="有女羅馬字", max_length=12, null=True)
  baxter = models.CharField(verbose_name="白一平轉寫", max_length=30, null=True)
  tcengh = models.CharField(verbose_name="推導中州音", max_length=30, null=True)  
  putonghua = models.CharField(verbose_name="推導普通話", max_length=12, null=True)
  
  class Meta:
    app_label = 'kyonh'

  def keys(self):
    return (
      'polyhedron', 
      'hiovNivv',
      'baxter',
      'tcengh',
      'putonghua',
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field(key).verbose_name
      value = self.__dict__[key]
      yield name, value

#廣韻目次
class KuangxYonhMiukTshiih(models.Model):
  #代表字
  dzih = models.CharField(max_length = 1, primary_key = True)
  #卷 上平 下平 上 去 入
  kyenh = models.CharField(max_length = 2)
  #廣韻韻目序號
  tshiih = models.SmallIntegerField()
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
    from ytenx.filters.templatetags.ytenx import sryoh
    return self.kyenh + u'聲' + sryoh(self.tshiih) + self.dzih;

#韻目
class YonhMiuk(models.Model):
  #代表字
  dzih = models.CharField(max_length = 2, primary_key = True)
  #所屬韻系
  gheh = models.ForeignKey('YonhGheh', db_index=True, on_delete=models.DO_NOTHING)
  #調
  deuh = models.SmallIntegerField()
  #廣韻目次
  tshiih = models.ForeignKey(KuangxYonhMiukTshiih, on_delete=models.DO_NOTHING)
  #韻母
  yonh = models.ManyToManyField('YonhMux')
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
    return self.dzih

#韻目集合
class YonhMiukDzip(models.Model):
  #平
  bieng = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+', on_delete=models.DO_NOTHING)
  #上
  dciangx = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+', on_delete=models.DO_NOTHING)
  #去
  khioh = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+', on_delete=models.DO_NOTHING)
  #入
  njip = models.OneToOneField('YonhMiuk', db_index=True, null=True, related_name='+', on_delete=models.DO_NOTHING)

  class Meta:
    app_label = 'kyonh'

  #韻系
  def gheh(self):
    if self.bieng: return self.bieng.gheh
    if self.dciangx: return self.dciangx.gheh
    if self.khioh: return self.khioh.gheh
    return self.njip.gheh

  #根據聲調獲取韻目
  def get_by_deuh(self, deuh):
    assert(deuh >=1 and deuh <= 4)
    if deuh == 1: return self.bieng
    if deuh == 2: return self.dciangx
    if deuh == 3: return self.khioh
    return self.njip

#十六韻攝
class YonhCjep(models.Model):
  #通江止遇蟹臻山效果假宕梗曾流深咸
  dzih = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
      return self.dzih;

#韻系
class YonhGheh(models.Model):
  #代表字
  dzih = models.CharField(max_length = 2, primary_key = True)
  #攝
  cjep = models.ForeignKey(YonhCjep, db_index = True, on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
      return self.dzih;


#反切上字
class DciangxDzih(models.Model):
  dzih = models.CharField(max_length = 1, primary_key = True)
  cjeng = models.ManyToManyField('CjengMux')
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
    return str(self.dzih)
  
  #反切
  def pyanx(self):
    return PyanxTshet.objects.filter(dciangx=self)
  
  #小韻
  def sieuxYonh(self):
    return SieuxYonh.objects.filter(pyanx__in=self.pyanx())

#反切下字
class GhraxDzih(models.Model):
  dzih = models.CharField(max_length = 1, primary_key = True)
  yonh = models.ManyToManyField('YonhMux')
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
    return str(self.dzih)
  
  #反切
  def pyanx(self):
    return PyanxTshet.objects.filter(ghrax=self)
  
  #小韻
  def sieuxYonh(self):
    return SieuxYonh.objects.filter(pyanx__in=self.pyanx())

#反切
class PyanxTshet(models.Model):
  #反切
  tshet = models.CharField(max_length = 2, primary_key = True)
  #反切上字
  dciangx = models.ForeignKey(DciangxDzih, db_index = True, on_delete=models.DO_NOTHING)
  #反切下字
  ghrax = models.ForeignKey(GhraxDzih, db_index = True, on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
    return self.dciangx.dzih + self.ghrax.dzih

  #小韻
  def sieuxYonh(self):
    return SieuxYonh.objects.filter(pyanx=self)


#擬音
class NgixQim(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=6)
  kauPuonxHanh = models.CharField(verbose_name="高本漢", max_length=16, null=True)
  lixPyangKueh = models.CharField(verbose_name="李方桂", max_length=16, null=True)
  yangLik = models.CharField(verbose_name="王力", max_length=16, null=True)
  tciuPyapKau = models.CharField(verbose_name="周法高", max_length=16, null=True)
  liukTcihYoi = models.CharField(verbose_name="陸志韋", max_length=16, null=True)
  tungxDungGhua = models.CharField(verbose_name="董同龢", max_length=16, null=True)
  lixYeng = models.CharField(verbose_name="李榮", max_length=16, null=True)
  dcjeuhYengPhyon = models.CharField(verbose_name="邵榮芬", max_length=16, null=True)
  drienghTriangDciangPyang = models.CharField(verbose_name="鄭張尚芳", max_length=16, null=True)
  phuanNgohYon = models.CharField(verbose_name="潘悟雲", max_length=16, null=True)
  boLipPuonx = models.CharField(verbose_name="蒲立本", max_length=16, null=True)
  
  class Meta:
    app_label = 'kyonh'

  def keys(self):
    return (
      'kauPuonxHanh',
      'lixPyangKueh', 
      'yangLik',
      'tciuPyapKau',
      'liukTcihYoi',
      'tungxDungGhua',
      'lixYeng',
      'dcjeuhYengPhyon',
      'drienghTriangDciangPyang',
      'phuanNgohYon', 
      'boLipPuonx',
    )

  def items(self): 
    for key in self.keys():
      name = self._meta.get_field(key).verbose_name
      value = self.__dict__[key]
      yield name, value

#單字條目
class Dzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index=True)
  #小韻
  sieuxYonh = models.ForeignKey('SieuxYonh', db_index=True, on_delete=models.DO_NOTHING)
  #小韻中位置
  yih = models.IntegerField(db_index=True)
  #字義
  ngieh = models.TextField()
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
      return self.dzih

#聲類
class CjengLyih(models.Model):
  #脣音 舌頭音 舌上音 齒頭音 正齒音莊組 正齒音章組 牙音 喉音 半舌音 半齒音
  mjeng = models.CharField(max_length = 5, primary_key = True)
  #序
  ziox = models.IntegerField()
  
  class Meta:
    app_label = 'kyonh'

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
  #拼音
  preng = models.OneToOneField('PrengQim', on_delete=models.DO_NOTHING)
  #序
  ziox = models.IntegerField()
  
  class Meta:
    app_label = 'kyonh'

  def __str__(self):
      return self.dzih
  
  #小韻
  def sieuxYonh(self):
      return SieuxYonh.objects.filter(cjeng=self)

#澤存堂本
class DrakDzuonDang(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=4)
  #卷
  kyenh = models.SmallIntegerField(db_index=True)
  #頁碼
  jep = models.SmallIntegerField(db_index=True)
  #文本
  myon = models.TextField()
  
  class Meta:
    app_label = 'kyonh'
  
  def __str__(self):
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
    if self.jep < max_jep[self.kyenh]:
      urls['next'] = base_path % (self.kyenh, self.jep + 1)
    
    return urls

#書
class Cio(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=4)
  #澤存堂本
  drakDzuonDang = models.OneToOneField(DrakDzuonDang, on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'kyonh'



class DeuhGhang:
  def __init__(self, miuk):
    self.miuk = miuk
    self.ho_ghang = []

class SieuxYonhManager(models.Manager):
  def get_yonh_do(self, dzip):
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
  cjeng = models.ForeignKey(CjengMux, db_index = True, on_delete=models.DO_NOTHING)
  #韻母
  yonh = models.ForeignKey(YonhMux, db_index = True, on_delete=models.DO_NOTHING)
  #韻目
  yonhMiuk = models.ForeignKey(YonhMiuk, db_index = True, on_delete=models.DO_NOTHING)
  #反切
  pyanx = models.ForeignKey(PyanxTshet, db_index = True, null = True, on_delete=models.DO_NOTHING)
  #擬音
  ngix = models.OneToOneField(NgixQim, on_delete=models.DO_NOTHING)
  #拼音
  preng = models.OneToOneField(PrengQim, related_name = 'preng', on_delete=models.DO_NOTHING)
  #推導音
  dauh = models.OneToOneField(PrengQim, related_name = 'dauh', on_delete=models.DO_NOTHING)
  #書
  cio = models.ManyToManyField(Cio)
  
  objects = SieuxYonhManager()
  
  class Meta:
    app_label = 'kyonh'

  def __str__(self):
    return self.taj

  #字
  def dzih(self):
    return Dzih.objects.filter(sieuxYonh = self)
  
  #聲調
  def deuh(self):
    return self.yonhMiuk.deuh
