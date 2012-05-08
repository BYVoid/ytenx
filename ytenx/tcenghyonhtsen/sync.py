# coding=utf-8
from django.http import HttpResponse
from models import *

basePath = './ytenx/tcenghyonhtsen/data/'
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
njipZiox = 1

def sync(request):
  syncYonhMiuk()
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

def syncYonhMiuk():
  print 'YonhMiuk...'

  def sync(line, num):
    global njipZiox
    ziox = num + 1
    #韻部
    bux = YonhBux(
      ziox = ziox,
      dzih = line[0][0],
    )
    bux.save()
    #韻目
    for i in range(1, 5):
      miuk = line[i]
      if not miuk: continue
      miuk = YonhMiuk(
        dzih = miuk,
        bux = bux,
        deuh = i,
        ziox = ziox,
      )
      #入聲
      if i == 4:
        miuk.ziox = njipZiox
        njipZiox += 1
      miuk.save()
      miukMap[miuk.dzih] = miuk

  traverse('YonhMiuk.txt', sync)
  print 'Done'

def syncPyanx(dciangx, ghrax):
  if (not ghrax) or (not ghrax):
    return None

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
    dzihDzip = line[11]
    koxDzip = line[12]
    jitDzip = line[13]
    if len(dzihDzip) >= 1:
      taj = dzihDzip[0]
    elif len(jitDzip) >= 1:
      taj = jitDzip[0]
    else:
      taj = koxDzip[0]
    
    miuk = miukMap[miuk]
    pyanx = syncPyanx(dciangx, ghrax)
    
    sieux = SieuxYonh(
      ziox = ziox,
      taj = taj,
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

