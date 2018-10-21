# coding=utf-8
from ytenx.tcenghyonhtsen.models import *

basePath = './ytenx/sync/tcenghyonhtsen/'
miukMap = {}
deuhMap = {
  u'平':1,
  u'上':2,
  u'去':3,
  u'入':4,
}
dciangxMap = {}
ghraxMap = {}
sieuxMap = {}
njipZiox = 1

def sync():
  syncYonhMiuk()
  syncSieux()
  syncDzih()
  syncKoxQim()
  syncJitDzih()
  syncSieuxCio()
  print 'Tcengh Yonh Tsen Done'

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
    taj = line[1]
    miuk = line[2]
    dciangx = line[3]
    ghrax = line[4]
    ipa = line[10]
    
    miuk = miukMap[miuk]
    pyanx = syncPyanx(dciangx, ghrax)
    
    sieux = SieuxYonh(
      ziox = ziox,
      taj = taj,
      yonhMiuk = miuk,
      pyanx = pyanx,
      ipa = ipa,
    )
    sieux.save()
    sieuxMap[ziox] = sieux
  
  traverse('SieuxYonh.txt', sync)
  print 'Done'

def syncDzih():
  print 'Dzih...'
  
  def sync(line, num):
    ziox = line[0]
    dzih = line[1]
    sieux = sieuxMap[line[2]]
    jeps = line[3]
    ngieh = line[4]

    dzih = Dzih(
      ziox = ziox,
      dzih = dzih,
      sieux = sieux,
      ngieh = ngieh,
    )
    
    kyenh = unicode(sieux.deuh())
    
    for jep in jeps.split('/'):
      cio = Cio(
        identifier = kyenh + jep,
        kyenh = kyenh,
        jep = jep,
      )
      cio.save()
      dzih.cio.add(cio)
    dzih.save()

  
  traverse('Dzih.txt', sync)
  print 'Done'

def syncKoxQim():
  print 'KoxQim...'
  
  def sync(line, num):
    ziox = line[0]
    dzih = line[1]
    sieux = sieuxMap[line[2]]
    jeps = line[3]

    dzih = KoxQim(
      ziox = ziox,
      dzih = dzih,
      sieux = sieux,
    )
    
    kyenh = unicode(sieux.deuh())
    
    for jep in jeps.split('/'):
      cio = Cio(
        identifier = kyenh + jep,
        kyenh = kyenh,
        jep = jep,
      )
      cio.save()
      dzih.cio.add(cio)
    dzih.save()

  
  traverse('KoxQim.txt', sync)
  print 'Done'

def syncJitDzih():
  print 'JitDzih...'
  
  def sync(line, num):
    ziox = line[0]
    dzih = line[1]
    sieux = sieuxMap[line[2]]
    jeps = line[3]

    dzih = JitDzih(
      ziox = ziox,
      dzih = dzih,
      sieux = sieux,
    )
    
    kyenh = unicode(sieux.deuh())
    
    for jep in jeps.split('/'):
      cio = Cio(
        identifier = kyenh + jep,
        kyenh = kyenh,
        jep = jep,
      )
      cio.save()
      dzih.cio.add(cio)
    dzih.save()

  traverse('JitDzih.txt', sync)
  print 'Done'

def syncSieuxCio():
  print 'SieuxCio...'
  for key in sieuxMap.keys():
    sieux = sieuxMap[key]
    
    cioMap = {}
    for dzih in sieux.dzih_set.all():
      for cio in dzih.cio.all():
        cioMap[cio.identifier] = cio
    for dzih in sieux.koxqim_set.all():
      for cio in dzih.cio.all():
        cioMap[cio.identifier] = cio
    for dzih in sieux.jitdzih_set.all():
      for cio in dzih.cio.all():
        cioMap[cio.identifier] = cio
    
    sieux.cio.clear()
    for key in cioMap.keys():
      cio = cioMap[key]
      sieux.cio.add(cio)
    sieux.save()

  print 'Done'
