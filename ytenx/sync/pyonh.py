# coding=utf-8
from ytenx.pyonh.models import *

basePath = './ytenx/sync/pyonh/'
cjengMuxMap = {}
yonhMuxMap = {}
cioMap = {}
sieuxYonhMap = {}

def sync():
  syncCjengMux()
  syncYonhMux()
  syncSieuxYonh()
  syncCio()
  syncDzih()
  syncSieuxCio()
  print('Pyonh Done')

def traverse(filename, callback):
  num = 0
  for line in open(basePath + filename):
    if (line[0] == '#'):
      continue
    line = line[:-1]
    line = line.split(' ')
    callback(line, num)
    num += 1

def syncCjengMux():
  print('CjengMux...')
  
  def sync(line, num):
    lyih = CjengLyih(
      mjeng = line[0]
    )
    lyih.save()
    
    dzih = line[1]
    
    # TODO NgixQim
    ngix = NgixQim(
      identifier = 'cjeng' + dzih,
    )
    ngix.save()
    
    cjeng = CjengMux(
      dzih = dzih,
      lyih = lyih,
      ngix = ngix,
    )
    cjeng.save()
    cjengMuxMap[dzih] = cjeng
  
  traverse('CjengMux.txt', sync)
  print('Done')

def syncYonhMux():
  print('YonhMux...')
  
  def sync(line, num):
    ziox = line[0]
    box = line[1]
    
    yonh_box = YonhBox(
      ziox = ziox,
      mjeng = box,
    )
    yonh_box.save()
    
    mjeng = box[0]
    # TODO NgixQim
    ngix = NgixQim(
      identifier = 'yonh' + mjeng,
    )
    ngix.save()
    
    yonh = YonhMux(
      mjeng = mjeng,
      yonh_box = yonh_box,
      tshyuk = False,
      ngix = ngix,
    )
    yonhMuxMap[mjeng] = yonh
    yonh.save()
    
    if len(box) == 4:
      mjeng = box[3]
      # TODO NgixQim
      ngix = NgixQim(
        identifier = 'yonh' + mjeng,
      )
      ngix.save()
      
      tshyuk_yonh = YonhMux(
        mjeng = mjeng,
        yonh_box = yonh_box,
        tshyuk = True,
        ngix = ngix,
        tuaih = yonh,
      )
      tshyuk_yonh.save()
      yonh.tuaih = tshyuk_yonh
      yonh.save()
      yonhMuxMap[mjeng] = tshyuk_yonh
      

  traverse('YonhBox.txt', sync)
  print('Done')

def syncSieuxYonh():
  print('SieuxYonh...')
  def sync(line, num):
    yonh = yonhMuxMap[line[3]]
    deuh = 0
    if line[5] == u'平':
      deuh = 1
    elif line[5] == u'上':
      deuh = 2
    elif line[5] == u'去':
      deuh = 3
    elif line[5] == u'入':
      deuh = 4
    else:
      assert(False)
    if deuh == 4:
      yonh = yonh.tuaih
  
    sieux = SieuxYonh(
      ziox = line[0],
      taj = line[1][0],
      cjeng = cjengMuxMap[line[2]],
      yonh_box = yonh.yonh_box,
      yonh = yonh,
      qim_jang = line[4] == u'陽',
      deuh = deuh,
    )
    sieux.save()
    sieuxYonhMap[line[0]] = sieux
  
  traverse('SieuxYonh.txt', sync)
  print('Done')

def syncCio():
  print('Cio...')
  
  for i in range(1, 106):
    identifier = '1_' + str(i)
    cio = Cio(
      identifier = identifier,
      kyenh = 1,
      jep = i,
    )
    cio.save()
    cioMap[identifier] = cio
  
  for i in range(1, 98):
    identifier = '2_' + str(i)
    cio = Cio(
      identifier = identifier,
      kyenh = 2,
      jep = i,
    )
    cio.save()
    cioMap[identifier] = cio
  
  print('Done')

def syncDzih():
  print('Dzih...')
  
  def sync(line, num):
    sieux = line[1]
    dzih = Dzih(
      ziox = line[0],
      sieux_yonh = sieuxYonhMap[sieux],
      dzih = line[2],
      ngieh = line[6],
    )
    
    if line[3] == u'上冊':
      vol = 1
    else:
      vol = 2
    identifier = str(vol) + '_' + line[4]
    dzih.cio.add(cioMap[identifier])
    if len(line[5]) > 0:
      identifier = str(vol) + '_' + line[5]
      dzih.cio.add(cioMap[identifier])  
    
    dzih.save()
  
  traverse('Dzih.txt', sync)
  print('Done')

def syncSieuxCio():
  print('SieuxCio...')
  for key in sieuxYonhMap.keys():
    sieux = sieuxYonhMap[key]
    
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
