# coding=utf-8
from ytenx.sync.common import traverse
from ytenx.dciangxkox.models import *
from ytenx.kyonh.models import SieuxYonh, PyanxTshet

base_path = './ytenx/sync/dciangx/'
cjeng_map = {}
yonh_map = {}
dzih_map = {}
last_dzih = None
myo = (u'魚孟', u'楚嫁', u'阻買')
mt = ''

def sync():
  syncDzih()
  print('Dciangx Done')

def syncDzih():
  print('Dzih...')
  
  def sync(line, num):
    global last_dzih, mt
    dzih = line[0]
    pyanx = line[7] + line[8]
    cjeng = line[9]
    yonh = line[10]
    yonh_seh = line[11]
    if yonh_seh == '':
      yonh_seh = 0
    
    if cjeng in cjeng_map:
      cjeng = cjeng_map[cjeng]
    else:
      cjeng = CjengByo(mjeng=cjeng)
      cjeng.save()
      cjeng_map[cjeng.mjeng] = cjeng
    
    if yonh in yonh_map:
      yonh = yonh_map[yonh]
    else:
      yonh = YonhBox(mjeng=yonh)
      yonh.save()
      yonh_map[yonh.mjeng] = yonh
    
    id = dzih
    i = 1
    while id in dzih_map:
      i += 1
      id = dzih + str(i)
    
    ngix_1 = line[12]
    ngix_2 = line[13]
    if len(ngix_2) == 0:
      ngix_2 = line[14]
      ngix_3 = line[15]
    else:
      ngix_3 = line[14]
      assert(len(line[15]) == 0)
    
    tshet = PyanxTshet.objects.filter(tshet = pyanx)
    sieux_yonh = None
    
    if len(tshet) == 1:
      tshet = tshet[0]
      sieuxs = SieuxYonh.objects.filter(pyanx = tshet)
      sieux_yonh = None
      for sieux in sieuxs:
        if sieux_yonh == None:
          sieux_yonh = sieux
        else:
          mt += str(num+2) + ' ' + dzih + ' ' + pyanx + ' ' + str(sieuxs) + '\n'
    else:
      if last_dzih.ngix_1 == ngix_1 and last_dzih.ngix_2 == ngix_2 and last_dzih.ngix_3 == ngix_3:
        sieux_yonh = last_dzih.sieux_yonh
      elif pyanx in myo:
        sieux_yonh = None
      elif dzih == u'拯' or dzih == u'氶':
        sieux_yonh = SieuxYonh.objects.get(ziox = 1919)
      else:
        mt += str(num+2) + ' ' + dzih + ' ' + pyanx + '\n'
    
    dzih = Dzih(
      ziox = num + 1,
      id = id,
      dzih = dzih,
      sieux_yonh = sieux_yonh,
      cjeng = cjeng,
      yonh = yonh,
      yonh_seh = yonh_seh,
      ngix_1 = ngix_1,
      ngix_2 = ngix_2,
      ngix_3 = ngix_3,
      tryoh = line[16],
    )
    
    dzih.save()
    dzih_map[dzih.id] = dzih
    last_dzih = dzih
  
  traverse(base_path + 'DrienghTriang.txt', sync)
  f = open('mt.txt', 'w')
  f.write(mt)
  f.close()
  print('Done')
