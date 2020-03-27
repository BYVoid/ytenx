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

sieuxZiox = {}
ziox = 0
f = open('JitDzih.txt', 'w')
maxZiox = 0
maxJep = 0

def sync(line, num):
  dzih = line[3]
  if len(dzih) == 0:
    return
  jep = line[4]
  if len(line[5]) != 0:
    jep = line[4] + '/' + line[5]
  
  pyanx = line[10] + line[11]
  preng = line[12] + line[13] + line[14]
  key = pyanx + preng
  print(key)
  ziox = sieuxZiox[key]
  
  output((dzih, ziox, jep))
  
  global maxJep
  jep = int(line[4])
  if jep < maxJep:
    print(dzih, line[2])
  maxJep = jep
  
  global maxZiox
  ziox = int(ziox)
  if ziox < maxZiox:
    print(dzih, line[2])
  maxZiox = ziox

def output(line):
  global ziox
  line = str(ziox) + ' ' + ' '.join(line) + '\n'
  ziox += 1
  line = line.encode('utf-8')
  f.write(line)

def sieux(line, num):
  ziox = line[0]
  pyanx = line[3] + line[4]
  preng = line[5] + line[6] + line[7]
  sieuxZiox[pyanx + preng] = ziox

traverse('SieuxYonh.txt', sieux)

output((u'字', u'小韻序號', u'頁碼'))
traverse('orig/JitDzih.txt', sync)
