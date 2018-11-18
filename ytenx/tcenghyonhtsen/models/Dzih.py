# coding=utf-8
from django.db import models
import re
import ytenx.kyonh.models

#單字條目
class Dzih(models.Model):
  gloss_fallback_pattern = u'(同上\([^\(\)]+)(\))'
  #Index in ytenx 
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True)
  #書頁
  cio = models.ManyToManyField('Cio')
  #字義
  ngieh = models.TextField();
  #對應廣韻小韻
  kwangx = models.ForeignKey(ytenx.kyonh.models.SieuxYonh, related_name='tcengh', null = True)
  #小韻于韻書中之序
  cioTriungZiox = models.IntegerField(db_index = True)

  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih
  
  def fallbackGloss(self, max_recursion_level = 3):
    if max_recursion_level == 0 or self.cioTriungZiox <= 1 or not re.match(Dzih.gloss_fallback_pattern, self.ngieh):
      return self.ngieh
    previous = Dzih.objects.filter(cioTriungZiox = self.cioTriungZiox - 1)
    if not previous:
      return self.ngieh
    return re.sub(Dzih.gloss_fallback_pattern, ur'\1‧' + previous.latest().fallbackGloss(max_recursion_level - 1) + ur'\2', self.ngieh)

#古音
class KoxQim(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True)
  #書頁
  cio = models.ManyToManyField('Cio');
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih

#逸字
class JitDzih(models.Model):
  #序號
  ziox = models.IntegerField(primary_key = True)
  #字
  dzih = models.CharField(max_length = 1, db_index = True)
  #小韻
  sieux = models.ForeignKey('SieuxYonh', db_index = True)
  #書頁
  cio = models.ManyToManyField('Cio');
  #字義
  ngieh = models.TextField();
  #對應廣韻小韻
  kwangx = models.ForeignKey(ytenx.kyonh.models.SieuxYonh, related_name='tcengh_jit', null = True)
  
  class Meta:
    app_label = 'tcenghyonhtsen'
  
  def __unicode__(self):
    return self.dzih
