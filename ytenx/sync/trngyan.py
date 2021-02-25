# coding=utf-8
from ytenx.sync.common import traverse
from ytenx.trngyan.models import *

base_path = './ytenx/sync/trngyan/'
cjeng_mux_ngix_qim = {}
cjeng_mux = {}
yonh_mux_ngix_qim = {}
yonh_mux = {}
cio_map = {}
sieux_yonh = {}
dzih_map = {}

def sync():
  syncCjengMuxNgixQim()
  syncCjengMux()
  syncYonhMuxNgixQim()
  syncYonhMux()
  syncSieuxYonh()
  syncCio()
  syncDzih()
  syncSieuxCio()
  print('Trngyan Done')

def syncCjengMuxNgixQim():
  print('CjengMuxNgixQim...')
  
  def sync(line, num):
    dzih = line[0]
    identifier = 'c' + dzih
    ngix = NgixQim(
      identifier = identifier,
      neng_keh_piuk = line[1],
    )
    ngix.save()
    cjeng_mux_ngix_qim[identifier] = ngix
  
  traverse(base_path + 'CjengMuxNgixQim.txt', sync)
  print('Done')

def syncCjengMux():
  print('CjengMux...')
  
  def sync(line, num):
    lyih = CjengLyih(
      mjeng = line[0]
    )
    lyih.save()
    
    dzih = line[1]
    ngix = cjeng_mux_ngix_qim['c' + dzih]
    
    cjeng = CjengMux(
      dzih = dzih,
      lyih = lyih,
      ngix = ngix,
    )
    cjeng.save()
    cjeng_mux[dzih] = cjeng
  
  traverse(base_path + 'CjengMux.txt', sync)
  print('Done')

def syncYonhMuxNgixQim():
  print('YonhMuxNgixQim...')
  
  def sync(line, num):
    mjeng = line[0]
    identifier = 'y' + mjeng
    ngix = NgixQim(
      identifier = identifier,
      neng_keh_piuk = line[1],
    )
    ngix.save()
    yonh_mux_ngix_qim[identifier] = ngix
  
  traverse(base_path + 'YonhMuxNgixQim.txt', sync)
  print('Done')

def syncYonhMux():
  print('YonhMux...')
  
  def sync(line, num):
    mjeng = line[0]
    box = mjeng[0:2]
    ho = mjeng[2]
    
    if ho == u'開':
      ho = 1
    elif ho == u'合':
      ho = 2
    elif ho == u'齊':
      ho = 3
    elif ho == u'撮':
      ho = 4
    else:
      assert(False)
    
    yonh_box = YonhBox(
      mjeng = box,
    )
    yonh_box.save()
    
    ngix = yonh_mux_ngix_qim['y' + mjeng]
    
    yonh = YonhMux(
      mjeng = mjeng,
      yonh_box = yonh_box,
      ho = ho,
      ngix = ngix,
    )
    yonh_mux[mjeng] = yonh
    yonh.save()

  traverse(base_path + 'YonhMux.txt', sync)
  print('Done')

def syncSieuxYonh():
  print('SieuxYonh...')
  def sync(line, num):
    deuh = line[2]
    if deuh == u'陰平':
      deuh = 1
    elif deuh == u'陽平':
      deuh = 2
    elif deuh == u'上':
      deuh = 3
    elif deuh == u'去':
      deuh = 4
    elif deuh == u'入平':
      deuh = 5
    elif deuh == u'入上':
      deuh = 6
    elif deuh == u'入去':
      deuh = 7
    else:
      assert(False)

    yonh = yonh_mux[line[5]]
    
    sieux = SieuxYonh(
      ziox = line[0],
      taj = line[1][0],
      cjeng = cjeng_mux[line[4]],
      yonh_box = yonh.yonh_box,
      yonh = yonh,
      deuh = deuh,
      ho = yonh.ho,
    )
    sieux.save()
    sieux_yonh[line[0]] = sieux
  
  traverse(base_path + 'TriungNgyanQimYonh.txt', sync)
  print('Done')

def syncCio():
  print('Cio...')
  
  for i in range(1, 94 + 1):
    identifier = '1_' + str(i)
    cio = Cio(
      identifier = identifier,
      kyenh = 1,
      jep = i,
    )
    cio.save()
    cio_map[identifier] = cio
  
  for i in range(1, 118 + 1):
    identifier = '2_' + str(i)
    cio = Cio(
      identifier = identifier,
      kyenh = 2,
      jep = i,
    )
    cio.save()
    cio_map[identifier] = cio
  
  print('Done')

def syncDzih():
  print('Dzih...')
  
  def sync(line, num):
    sieux_ziox = line[0]
    dzih = line[1]
    
    id = dzih
    i = 1
    while id in dzih_map:
      i += 1
      id = dzih + str(i)
    
    dzih = Dzih(
      ziox = num + 1,
      id = id,
      sieux_yonh = sieux_yonh[sieux_ziox],
      dzih = dzih,
      tryoh = line[3],
    )
    
    identifier = '1_' + line[2]
    dzih.cio.add(cio_map[identifier])
    
    dzih.save()
    dzih_map[dzih.id] = dzih_map
  
  traverse(base_path + 'Dzih.txt', sync)
  print('Done')

def syncSieuxCio():
  print('SieuxCio...')
  for key in sieux_yonh.keys():
    sieux = sieux_yonh[key]
    
    cioTmp = {}
    for dzih in sieux.dzih_set.all():
      for cio in dzih.cio.all():
        cioTmp[cio.identifier] = cio
    
    sieux.cio.clear()
    for key in cioTmp.keys():
      cio = cioTmp[key]
      sieux.cio.add(cio)
    sieux.save()

  print('Done')
