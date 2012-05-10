# coding=utf-8

def traverse(filename, callback):
  num = 0
  for line in open(filename):
    if (line[0] == '#'):
      continue
    line = line[:-1].decode('utf-8')
    line = line.split(' ')
    callback(line, num)
    num += 1

adl = []
ziox = 0
f = open('Sieux.txt', 'w')

def sync(line, num):
  miuk = line[2][-1]
  dciangx = line[6]
  ghrax = line[7]
  cjeng = line[8]
  yonh = line[9]
  deuh = line[10]
  
  dzih = line[12]
  kox = line[13]
  koxziox = line[14]
  jit = line[15]
  jitziox = line[16]
  
  ad = False
  if len(dzih) > 0:
    taj = dzih[0]
  elif len(kox) > 0:
    taj = kox[0]
    ad = True
  else:
    taj = jit[0]
    ad = True
  
  line = (taj, miuk, dciangx, ghrax, cjeng, yonh, deuh, koxziox, jitziox)
  if ad:
    adl.append(line)
  else:
    output(line)

def output(line):
  global ziox
  line = str(ziox) + ' ' + ' '.join(line) + '\n'
  ziox += 1
  line = line.encode('utf-8')
  f.write(line)

output((u'代表字', u'韻目', u'反切上字', u'反切下字', u'聲母', u'韻母', u'韻母', u'聲調', u'古音序', u'逸字序'))
traverse('SieuxYonh.txt', sync)
for line in adl:
  output(line)
