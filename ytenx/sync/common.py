# coding=utf-8

def traverse(filename, separator, callback):
  num = 0
  for line in open(filename):
    if (line[0] == '#'):
      continue
    line = line[:-1]
    line = line.decode('utf-8')
    line = line.split(separator)
    callback(line, num)
    num += 1
