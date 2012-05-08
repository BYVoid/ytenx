# coding=utf-8
from django.http import HttpResponse
from models import *

basePath = './ytenx/tcenghyonhtsen/data/'
buxMap = {}
miukMap = {}
deuhMap = {
  u'平':1,
  u'上':2,
  u'去':3,
  u'入':4,
}
dciangxMap = {}
ghraxMap = {}
dzihZiox = 1
koxZiox = 1
jitZiox = 1

def sync(request):
  syncSieux()
  return HttpResponse('Done.\n')

def traverse(filename, callback):
  num = 0
  for line in open(basePath + filename):
    if (line[0] == '#'):
      continue
    line = line[:-1].decode('utf-8')
    line = line.split(' ')
    callback(line, num)
    num += 1

def syncMiuk(miuk, buxnum, deuh):
  #韻部
  if buxMap.has_key(buxnum):
    bux = buxMap[buxnum]
  else:
    bux = YonhBux(dzih = miuk)
    bux.save()
    buxMap[buxnum] = bux
  
  #韻目
  miuk = YonhMiuk(
    dzih = miuk,
    bux = bux,
    deuh = deuh,
  )
  miuk.save()
  miukMap[miuk.dzih] = miuk

def syncPyanx(dciangx, ghrax):
  #反切上字
  if dciangxMap.has_key(dciangx):
    dciangx = dciangxMap[dciangx]
  else:
    dciangx = DciangxDzih(dzih = dciangx)
    dciangx.save()
    dciangxMap[dciangx] = dciangx
  
  #反切下字
  if ghraxMap.has_key(ghrax):
    ghrax = ghraxMap[ghrax]
  else:
    ghrax = GhraxDzih(dzih = ghrax)
    ghrax.save()
    ghraxMap[dciangx] = ghrax

  pyanx = PyanxTshet(
    tshet = dciangx.dzih + ghrax.dzih,
    dciangx = dciangx,
    ghrax = ghrax,
  )
  pyanx.save()
  return pyanx

def syncSieux():
  print 'Sieux...'
  
  def sync(line, num):
    ziox = line[0]
    miuk = line[1][-1]
    buxnum = line[2]
    deuh = deuhMap[line[3]]
    dciangx = line[5]
    ghrax = line[6]
    dzihDzip = line[10]
    koxDzip = line[11]
    jitDzip = line[12]
    
    if not miukMap.has_key(miuk):
      syncMiuk(miuk, buxnum, deuh)
    miuk = miukMap[miuk]
    
    pyanx = syncPyanx(dciangx, ghrax)
    
    sieux = SieuxYonh(
      ziox = ziox,
      taj = dzihDzip[0],
      yonhMiuk = miuk,
      pyanx = pyanx,
    )
    sieux.save()
    
    yih = 1
    global dzihZiox
    for dzih in dzihDzip:
      dzih = Dzih(
        ziox = dzihZiox,
        dzih = dzih,
        yih = yih,
        sieux = sieux,
      )
      dzih.save()
      dzihZiox += 1
      yih += 1
    
    global koxZiox
    for dzih in koxDzip:
      dzih = KoxQim(
        ziox = koxZiox,
        dzih = dzih,
        sieux = sieux,
      )
      dzih.save()
      koxZiox += 1
    
    global jitZiox
    for dzih in jitDzip:
      dzih = JitDzih(
        ziox = jitZiox,
        dzih = dzih,
        sieux = sieux,
      )
      dzih.save()
      jitZiox += 1
  
  traverse('tcenghyonhtsen.txt', sync)
  print 'Done'

