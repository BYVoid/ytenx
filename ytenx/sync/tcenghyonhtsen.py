# coding=utf-8
from ytenx.tcenghyonhtsen.models import *
import ytenx.kyonh.models

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
cioTriungSieuxZiox = 1
cioTriungDzihZiox = 1

def sync():
  syncYonhMiuk()
  syncSieux()
  syncQimBjin()
  syncDzih()
  syncKoxQim()
  syncJitDzih()
  syncSieuxCio()
  syncTranscriptionLegend()
  print('Tcengh Yonh Tsen Done')

def traverse(filename, callback, separator = ' '):
  num = 0
  for line in open(basePath + filename):
    if (line[0] == '#'):
      continue
    line = line[:-1]
    line = line.split(separator)
    callback(line, num)
    num += 1

def syncYonhMiuk():
  print('YonhMiuk...')

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
  print('Done')

def syncPyanx(dciangx, ghrax):
  if (not ghrax) or (not ghrax):
    return None

  #反切上字
  if dciangx in dciangxMap:
    dciangx = dciangxMap[dciangx]
  else:
    dciangx = DciangxDzih(dzih = dciangx)
    dciangx.save()
    dciangxMap[dciangx] = dciangx
  
  #反切下字
  if ghrax in ghraxMap:
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
  print('Sieux...')
  
  def sync(line, num):
    global cioTriungSieuxZiox
    ziox = line[0]
    taj = line[1]
    miuk = line[2]
    dciangx = line[3]
    ghrax = line[4]
    ipa = line[10]
    jamo = line[11]    
    
    miuk = miukMap[miuk]
    pyanx = syncPyanx(dciangx, ghrax)
    
    sieux = SieuxYonh(
      ziox = ziox,
      taj = taj,
      yonhMiuk = miuk,
      pyanx = pyanx,
      ipa = ipa,
      jamo = jamo,
      cioTriungZiox = cioTriungSieuxZiox,
    )
    cioTriungSieuxZiox = cioTriungSieuxZiox + 1
    sieux.save()
    sieuxMap[ziox] = sieux
  
  traverse('SieuxYonh.txt', sync)
  print('Done')

def syncQimBjin():
  print('QimBjin...')

  def getSieuxYonhOrNone(i):
    if i == '?' or i == '':
      return None
    return sieuxMap[i]
 
  def sync(line, num):
    ziox = line[0]
    t1 = getSieuxYonhOrNone(line[1])
    t2 = getSieuxYonhOrNone(line[2])
    t3 = getSieuxYonhOrNone(line[3])
    t4 = getSieuxYonhOrNone(line[4])
    merge_t2_t3 = (line[5] != "FALSE")
    has_t4 = (line[4] != '')
    filename = line[6]
    additional = getSieuxYonhOrNone(line[7])
    
    qimBjin = QimBjin(
      ziox = ziox,
      t1 = t1,
      t2 = t2,
      t3 = t3,
      t4 = t4,
      merge_t2_t3 = merge_t2_t3,
      has_t4 = has_t4,
      filename = filename,
      additional = additional,
    )
    qimBjin.save()
  
  traverse('QimBjin.txt', sync)
  print('Done')

def syncDzih():
  print('Dzih...')
  
  def sync(line, num):
    global cioTriungDzihZiox
    ziox = line[0]
    dzih = line[1]
    sieux = sieuxMap[line[2]]
    jeps = line[3]
    ngieh = line[4]
    kwangx = None;
    if len(line) > 5 and len(line[5]) > 0:
      try:
        kwangx = ytenx.kyonh.models.SieuxYonh.objects.get(ziox = line[5])
      except:
        pass

    dzih = Dzih(
      ziox = ziox,
      dzih = dzih,
      sieux = sieux,
      ngieh = ngieh,
      kwangx = kwangx,
      cioTriungZiox = cioTriungDzihZiox,
    )
    cioTriungDzihZiox = cioTriungDzihZiox + 1
    
    kyenh = str(sieux.deuh())
    
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
  print('Done')

def syncKoxQim():
  print('KoxQim...')
  
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
    
    kyenh = str(sieux.deuh())
    
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
  print('Done')

def syncJitDzih():
  print('JitDzih...')
  
  def sync(line, num):
    ziox = line[0]
    dzih = line[1]
    sieux = sieuxMap[line[2]]
    jeps = line[3]
    ngieh = line[4]
    kwangx = None;
    if len(line) > 5 and len(line[5]) > 0:
      try:
        kwangx = ytenx.kyonh.models.SieuxYonh.objects.get(ziox = line[5])
      except:
        pass

    dzih = JitDzih(
      ziox = ziox,
      dzih = dzih,
      sieux = sieux,
      ngieh = ngieh,
      kwangx = kwangx,      
    )
    
    kyenh = str(sieux.deuh())
    
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
  print('Done')

def syncSieuxCio():
  print('SieuxCio...')
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

  print('Done')

def syncTranscriptionLegend():
  print('Transcription...')
  
  def syncGhiunh(line, num):
    ghiunh = GhiunhTranscription(
      ziox = line[0],
      ghiunhBox = line[1],
      shioJiekHiunh = line[2],
      shioIpa = line[3],
      njipJiekHiunh = line[4],
      njipIpa = line[5],
    )
    ghiunh.save()
    
  def syncShieng(line, num):
    shieng = ShiengTranscription(
      ziox = line[0],
      shiengLwih = line[1],
      jiekHiunh = line[2],
      ipa = line[3],
      memo = line[4],
    )
    shieng.save()
    
  def syncDewh(line, num):
    dewh = DewhTranscription(
      ziox = line[0],
      dewhLwih = line[1],
      jiekHiunh = line[2],
      ipa = line[3],
      memo = line[4],
    )
    dewh.save()    

  traverse('GhiunhTranscription.txt', syncGhiunh, separator='\t')
  traverse('ShiengTranscription.txt', syncShieng, separator='\t')
  traverse('DewhTranscription.txt', syncDewh, separator='\t')
  print('Done')
  
