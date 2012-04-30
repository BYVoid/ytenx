# coding=utf-8
from django.http import HttpResponse
from models import *

basePath = './ytenx/kyonh/data/'
cjengMuxPrengQimMap = {}
cjengMuxNgixQimMap = {}
cjengMuxMap = {}
ghehMap = {}
yonhMuxPrengQimMap = {}
yonhMuxNgixQimMap = {}
yonhMuxMap = {}
kuangxYonhMiukTshiihMap = {}
yonhMiukMap = {}
drakDzuonDangMap = {}
cioMap = {}
pyanxTshetDciangxDzihMap = {}
pyanxTshetGhraxDzihMap = {}
pyanxTshetMap = {}
prengQimMap = {}
ngixQimMap = {}
sieuxYonhMap = {}

def sync(request):
  syncCjengMuxPrengQim()
  syncCjengMuxNgixQim()
  syncCjengMux()
  syncYonhGheh()
  syncYonhMuxPrengQim()
  syncYonhMuxNgixQim()
  syncYonhMux()
  syncPrengQim()
  syncNgixQim()
  syncPyanxTshet()
  syncKuangxYonhMiukTshiih()
  syncYonhMiuk()
  syncDrakDzuonDang()
  syncCio()
  syncSieuxYonh()
  syncDzih()
  syncDciangxDzihCjeng()
  syncGhraxDzihYonh()
  return HttpResponse('Done.\n')

def traverse(filename, callback):
  num = 0
  for line in open(basePath + filename):
    if (line[0] == '#'):
      continue
    line = line[:-1]
    line = line.split(' ')
    callback(line, num)
    num += 1

def syncCjengMuxPrengQim():
  print 'CjengMuxPrengQim...'
  
  def sync(line, num):
    preng = PrengQim(
      identifier = '聲母' + line[0],
      polyhedron = line[1],
      thuaiDauh = line[2],
    )
    preng.save()
    cjengMuxPrengQimMap[line[0]] = preng
  
  traverse('CjengMuxPrengQim.txt', sync)
  print 'Done'

def syncCjengMuxNgixQim():
  print 'CjengMuxNgixQim...'
  
  def sync(line, num):
    ngix = NgixQim(
      identifier = '聲母' + line[0],
      kauPuonxHanh = line[1],
      lixPyangKueh = line[2],
      yangLik = line[3],
      tciuPyapKau = line[4],
      liukTcihYoi = line[5],
      tungxDungGhua = line[6],
      lixYeng = line[7],
      dcjeuhYengPhyon = line[8],
      drienghTriangDciangPyang = line[9],
      phuanNgohYon = line[10],
      boLipPuonx = line[11],
    )
    ngix.save()
    cjengMuxNgixQimMap[line[0]] = ngix
  
  traverse('CjengMuxNgixQim.txt', sync)
  print 'Done'

def syncCjengMux():
  print 'CjengMux...'
  
  def sync(line, num):
    lyih = CjengLyih(
      mjeng = line[1]
    )
    lyih.save()
    cjeng = CjengMux(
      dzih = line[0],
      lyih = lyih,
      ngix = cjengMuxNgixQimMap[line[0]],
      preng = cjengMuxPrengQimMap[line[0]],
    )
    cjeng.save()
    cjengMuxMap[line[0]] = cjeng
  
  traverse('CjengMux.txt', sync)
  print 'Done'

def syncYonhGheh():
  print 'YonhGheh...'
  
  def sync(line, num):
    cjep = YonhCjep(
      dzih = line[1],
    )
    cjep.save()
  
    gheh = YonhGheh(
      dzih = line[0],
      cjep = cjep,
    )
    gheh.save()
    ghehMap[line[0]] = gheh
    
  traverse('YonhGheh.txt', sync)
  print 'Done'

def syncYonhMuxPrengQim():
  print 'YonhMuxPrengQim...'
  
  def sync(line, num):
    preng = PrengQim(
      identifier = '韻母' + line[0],
      polyhedron = line[1],
      thuaiDauh = line[2],
    )
    preng.save()
    yonhMuxPrengQimMap[line[0]] = preng
  
  traverse('YonhMuxPrengQim.txt', sync)
  print 'Done'

def syncYonhMuxNgixQim():
  print 'YonhMuxNgixQim...'
  
  def sync(line, num):
    ngix = NgixQim(
      identifier = '韻母' + line[0],
      kauPuonxHanh = line[1],
      yangLik = line[2],
      lixYeng = line[3],
      dcjeuhYengPhyon = line[4],
      drienghTriangDciangPyang = line[5],
      phuanNgohYon = line[6],
      boLipPuonx = line[7],
    )
    ngix.save()
    yonhMuxNgixQimMap[line[0]] = ngix
  
  traverse('YonhMuxNgixQim.txt', sync)
  print 'Done'

def syncYonhMux():
  print 'YonhMux...'
  
  def sync(line, num):
    ho = line[3] == '開'
    tshyuk = line[4] == '促'
    yonh = YonhMux(
      mjeng = line[0],
      gheh = ghehMap[line[1]],
      tongx = line[2],
      ho = ho,
      tshyuk = tshyuk,
      ngix = yonhMuxNgixQimMap[line[0]],
      preng = yonhMuxPrengQimMap[line[0]],
    )
    yonh.save()
    yonhMuxMap[line[0]] = yonh

  def syncTuaih(line, num):
    tuaih = line[5]
    if tuaih == '': return
    yonh = yonhMuxMap[line[0]]
    tuaih = yonhMuxMap[tuaih]
    yonh.tuaih = tuaih
    yonh.save()

  traverse('YonhMux.txt', sync)
  traverse('YonhMux.txt', syncTuaih)
  print 'Done'

def syncPyanxTshet():
  print 'PyanxTshet...'
  
  def sync(line, num):
    tshet = line[5].decode('utf-8')
    if not tshet: return
    dciangxDzih = DciangxDzih(
      dzih = tshet[0],
    )
    dciangxDzih.save()
    pyanxTshetDciangxDzihMap[dciangxDzih.dzih] = dciangxDzih
    
    ghraxDzih = GhraxDzih(
      dzih = tshet[1],
    )
    ghraxDzih.save()
    pyanxTshetGhraxDzihMap[ghraxDzih.dzih] = ghraxDzih
    
    dzih = PyanxTshet(
      tshet = tshet,
      dciangx = dciangxDzih,
      ghrax = ghraxDzih,
    )
    dzih.save()
    pyanxTshetMap[tshet.encode('utf-8')] = dzih
  
  traverse('SieuxYonh.txt', sync)
  print 'Done'

def syncKuangxYonhMiukTshiih():
  print 'KuangxYonhMiukTshiih...'
  
  def sync(line, num):
    tshiih = KuangxYonhMiukTshiih(
      dzih = line[0],
      kyenh = line[1],
      tshiih = line[2],
    )
    tshiih.save()
    kuangxYonhMiukTshiihMap[line[0]] = tshiih
  
  traverse('KuangxYonhMiukTshiih.txt', sync)
  print 'Done'

def syncYonhMiuk():
  print 'YonhMiuk...'
  
  def sync(line, num):
    yonh = YonhMiuk(
      dzih = line[0],
      gheh = ghehMap[line[1]],
      deuh = line[2],
      tshiih = kuangxYonhMiukTshiihMap[line[3]]
    )
    
    yonh.yonh.clear()
    for key in yonhMuxMap.keys():
      yonhMux = yonhMuxMap[key]
      if yonhMux.gheh == yonh.gheh and yonhMux.tshyuk == (yonh.deuh == 4):
        yonh.yonh.add(yonhMux)
    
    yonh.save()
    yonhMiukMap[line[0]] = yonh
  
  traverse('YonhMiuk.txt', sync)
  print 'Done'

def syncDrakDzuonDang():
  print 'DrakDzuonDang...'
  
  def sync(line, num):
    id = line[0] + '_' + line[1]
    drak = DrakDzuonDang(
      identifier = id,
      kyenh = line[0],
      jep = line[1],
    )
    drak.save()
    drakDzuonDangMap[id] = drak
  
  traverse('DrakDzuonDang.txt', sync)
  print 'Done'

def syncCio():
  print 'Cio...'
  
  for key in drakDzuonDangMap.keys():
    drak = drakDzuonDangMap[key]
    cio = Cio(
      identifier = drak.identifier,
      drakDzuonDang = drak,
    )
    cio.save()
    cioMap[drak.identifier] = cio
  
  print 'Done'

def syncNgixQim():
  print 'NgixQim...'
  
  def sync(line, num):
    ngix = NgixQim(
      identifier = line[0],
    )
    cjeng = cjengMuxMap[line[2]]
    yonh = yonhMuxMap[line[3]]
    for key in cjeng.ngix.keys():
      if hasattr(cjeng.ngix, key) and hasattr(yonh.ngix, key):
        cjengNgix = getattr(cjeng.ngix, key)
        yonhNgix = getattr(yonh.ngix, key)
        if cjengNgix and yonhNgix:
          setattr(ngix, key, cjengNgix + yonhNgix)

    ngix.save()
    ngixQimMap[line[0]] = ngix
  
  traverse('SieuxYonh.txt', sync)
  
  print 'Done'

def syncPrengQim():
  print 'PrengQim...'
  
  def sync(line, num):
    id = line[0]
    preng = PrengQim(
      identifier = id,
      thuaiDauh = line[1],
      polyhedron = line[2],
      hiovNivv = line[3],
    )
    preng.save()
    prengQimMap[id] = preng
  
  traverse('PrengQim.txt', sync)
  print 'Done'

def syncSieuxYonh():
  print 'SieuxYonh...'
  def sync(line, num):
    if line[5] != '':
      pyanx = pyanxTshetMap[line[5]]
    else:
      pyanx = None
    sieux = SieuxYonh(
      ziox = line[0],
      taj = line[1],
      cjeng = cjengMuxMap[line[2]],
      yonh = yonhMuxMap[line[3]],
      yonhMiuk = yonhMiukMap[line[4]],
      pyanx = pyanx,
      ngix = ngixQimMap[line[0]],
      preng = prengQimMap[line[0]],
    )
    sieux.cio.clear()
    for cio in line[6].split('/'):
      sieux.cio.add(cioMap[cio])
    sieux.save()
    sieuxYonhMap[line[0]] = sieux
  
  traverse('SieuxYonh.txt', sync)
  print 'Done'

def syncDzih():
  print 'Dzih...'
  
  def sync(line, num):
    dzih = Dzih(
      ziox = num + 1,
      dzih = line[0],
      sieuxYonh = sieuxYonhMap[line[1]],
      yih = line[2],
      ngieh = line[3],
    )
    dzih.save()
  
  traverse('Dzih.txt', sync)
  print 'Done'

def syncDciangxDzihCjeng():
  print 'DciangxDzihCjeng...'
  for i in pyanxTshetDciangxDzihMap.keys():
    dciangx = pyanxTshetDciangxDzihMap[i]
    #查詢以該上字爲反切的所有小韻的聲母
    cjengM = {}
    for j in sieuxYonhMap.keys():
      sieux = sieuxYonhMap[j]
      if not sieux.pyanx: continue
      if sieux.pyanx.dciangx == dciangx:
        cjengM[sieux.cjeng.dzih] = sieux.cjeng
    dciangx.cjeng.clear()
    for j in cjengM.keys():
      cjeng = cjengM[j]
      dciangx.cjeng.add(cjeng)
    dciangx.save()
  print 'Done'

def syncGhraxDzihYonh():
  print 'GhraxDzihYonh...'
  for i in pyanxTshetGhraxDzihMap.keys():
    ghrax = pyanxTshetGhraxDzihMap[i]
    #查詢以該下字爲反切的所有小韻的韻母
    yonhM = {}
    for j in sieuxYonhMap.keys():
      sieux = sieuxYonhMap[j]
      if not sieux.pyanx: continue
      if sieux.pyanx.ghrax == ghrax:
        yonhM[sieux.yonh.mjeng] = sieux.yonh
    ghrax.yonh.clear()
    for j in yonhM.keys():
      yonh = yonhM[j]
      ghrax.yonh.add(yonh)
    ghrax.save()
  print 'Done'
