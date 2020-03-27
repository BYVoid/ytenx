# coding=utf-8
import re
from django.db import models
from ytenx.kyonh.models import SieuxYonh as KyonhSieuxYonh
from ytenx.filters.templatetags.ytenx import sryoh

#書
class Cio(models.Model):
  #標識
  identifier = models.CharField(primary_key=True, max_length=5)
  #卷
  kyenh = models.SmallIntegerField(db_index=True)
  #頁碼
  jep = models.SmallIntegerField(db_index=True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'

  def __str__(self):
    return '%d-%d' % (self.kyenh, self.jep)
  
  def filename(self):
    return '%03d' % self.jep + '.jpg'

#單字條目
class Dzih(models.Model):
  gloss_fallback_pattern = u'(同上[（\(][^（）\(\)]+)([）\)])'
  #Index in ytenx 
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True, on_delete=models.DO_NOTHING)
  #書頁
  cio = models.ManyToManyField('Cio')
  #字義
  ngieh = models.TextField();
  #對應廣韻小韻
  kwangx = models.ForeignKey(KyonhSieuxYonh, related_name='tcengh', null = True, on_delete=models.DO_NOTHING)
  #小韻于韻書中之序
  cioTriungZiox = models.IntegerField(db_index = True)

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.dzih
  
  def fallbackGloss(self, max_recursion_level = 8):
    if max_recursion_level == 0 or self.cioTriungZiox <= 1 or not re.match(Dzih.gloss_fallback_pattern, self.ngieh):
      return self.ngieh
    previous = Dzih.objects.filter(cioTriungZiox = self.cioTriungZiox - 1)
    if not previous:
      return self.ngieh
    return re.sub(Dzih.gloss_fallback_pattern, r'\1‧' + previous[:1][0].fallbackGloss(max_recursion_level - 1) + r'\2', self.ngieh)

#古音
class KoxQim(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True, on_delete=models.DO_NOTHING)
  #書頁
  cio = models.ManyToManyField('Cio');
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.dzih

#逸字
class JitDzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True, on_delete=models.DO_NOTHING)
  #書頁
  cio = models.ManyToManyField('Cio');
  #字義
  ngieh = models.TextField();
  #對應廣韻小韻
  kwangx = models.ForeignKey(KyonhSieuxYonh, related_name='tcengh_jit', null = True, on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.dzih

#反切上字
class DciangxDzih(models.Model):
  dzih = models.CharField(max_length = 1, primary_key = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
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
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
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
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.dciangx.dzih + self.ghrax.dzih

#小韻
class QimBjin(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #平聲小韻號
  t1 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_1', db_index = True, null = True, on_delete=models.DO_NOTHING)
  #上聲小韻號
  t2 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_2', db_index = True, null = True, on_delete=models.DO_NOTHING)
  #去聲小韻號
  t3 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_3', db_index = True, null = True, on_delete=models.DO_NOTHING)
  #入聲小韻號
  t4 = models.ForeignKey('SieuxYonh', related_name='qim_bjin_4', db_index = True, null = True, on_delete=models.DO_NOTHING)
  #重上聲是否歸于去聲
  merge_t2_t3 = models.BooleanField();
  #是否可有入聲
  has_t4 = models.BooleanField();
  #文件名
  filename = models.CharField(max_length = 16, db_index = True);
  #增補小韻號
  additional = models.ForeignKey('SieuxYonh', related_name='qim_bjin_additional', db_index = True, null = True, on_delete=models.DO_NOTHING)
  
  class Meta:
    app_label = 'tcenghyonhtsen'

  def __str__(self):
    mapping = self.tone_to_ipa_mapping()
    text = u''
    for tone, ipa in mapping:
      text = text + tone + ipa + ' '
    return text

  def tone_to_ipa_mapping(self):
    def getIPA(sieuxYonh):
        if sieuxYonh is None:
          return u'?'
        ipa = sieuxYonh.ipa
        ipa = re.sub(u'^\(ŋ\)|\'$', u'', ipa)
        ipa = re.sub(u'iɪ(.?)i', r'i\1', ipa)
        return ipa
    
    result = [(u'平', getIPA(self.t1))]
    if self.merge_t2_t3:
      result.append((u'上去', getIPA(self.t2 if self.t3 is None else self.t3)))
    else:
      result.append((u'上', getIPA(self.t2)))
      result.append((u'去', getIPA(self.t3)))
    if self.has_t4:
      result.append((u'入', getIPA(self.t4)))
    return result

#小韻
class SieuxYonh(models.Model):
  #Permanent index in ytenx
  ziox = models.IntegerField(primary_key = True)
  #代表字
  taj = models.CharField(max_length = 1, db_index = True)
  #韻目
  yonhMiuk = models.ForeignKey('YonhMiuk', db_index = True, on_delete=models.DO_NOTHING)
  #反切
  pyanx = models.ForeignKey('PyanxTshet', db_index = True, null = True, on_delete=models.DO_NOTHING)
  #書頁
  cio = models.ManyToManyField('Cio')
  #彥文
  jamo = models.CharField(max_length = 16, db_index = True);
  #IPA
  ipa = models.CharField(max_length = 16, db_index = True);
  #小韻于韻書中之序
  cioTriungZiox = models.IntegerField(db_index = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'

  def __str__(self):
    return self.taj
  
  #聲調
  def deuh(self):
    return self.yonhMiuk.deuh

  def ziox_cio(self):
    return self.cio.order_by('kyenh').order_by('jep').all()
  
  def qim_bjin_list(self):
    normal_set = self.qim_bjin_1.all() | self.qim_bjin_2.all() | self.qim_bjin_3.all() | self.qim_bjin_4.all()
    unique_normal_list = list(normal_set)[0:1] if normal_set else []
    return unique_normal_list + list(self.qim_bjin_additional.all())



#韻母轉寫
class GhiunhTranscription(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #韻部
  ghiunhBox = models.CharField(max_length = 4)
  #譯訓舒聲
  shioJiekHiunh = models.CharField(max_length = 8)
  #舒聲IPA轉寫
  shioIpa = models.CharField(max_length = 16)
  #譯訓舒聲
  njipJiekHiunh = models.CharField(max_length = 8)
  #舒聲IPA轉寫
  njipIpa = models.CharField(max_length = 16)

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.shioIpa

#聲母轉寫
class ShiengTranscription(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #聲類
  shiengLwih = models.CharField(max_length = 4)
  #譯訓
  jiekHiunh = models.CharField(max_length = 8)
  #IPA轉寫
  ipa = models.CharField(max_length = 16)
  #備註
  memo = models.TextField();

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.ipa

#聲調轉寫
class DewhTranscription(models.Model):
  #序
  ziox = models.IntegerField(primary_key = True)
  #調類
  dewhLwih = models.CharField(max_length = 4)
  #譯訓
  jiekHiunh = models.CharField(max_length = 8)
  #IPA轉寫
  ipa = models.CharField(max_length = 16)
  #備註
  memo = models.TextField();

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.ipa

#韻部
class YonhBux(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #代表字
  dzih = models.CharField(max_length = 2, unique = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return self.dzih;
  
  def miuk(self):
    dzip = {}
    for yonh in self.yonhmiuk_set.all():
      if yonh.deuh == 1:
        dzip['bieng'] = yonh
      elif yonh.deuh == 2:
        dzip['dciangx'] = yonh
      elif yonh.deuh == 3:
        dzip['khioh'] = yonh
      elif yonh.deuh == 4:
        dzip['njip'] = yonh
    return dzip

#韻目
class YonhMiuk(models.Model):
  #序號
  ziox = models.IntegerField()
  #代表字
  dzih = models.CharField(max_length = 2, primary_key = True)
  #韻部
  bux = models.ForeignKey('YonhBux', db_index = True, on_delete=models.DO_NOTHING)
  #調
  deuh = models.SmallIntegerField()
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __str__(self):
    return sryoh(self.ziox) + self.dzih

  def cio(self):
    cio_map = {}
    for sieux in self.sieuxyonh_set.all():
      for cio in sieux.cio.all():
        cio_map[cio.identifier] = cio
    cio = list(cio_map.values())
    cio.sort(key=lambda x: (x.kyenh, x.jep))
    print(cio)
    return cio
