# coding=utf-8

def traverse(filename, callback, **kwargs):
  num = 0
  separator = ' '
  if kwargs.has_key('separator'):
    separator = kwargs['separator']
  for line in open(filename):
    if (line[0] == '#'):
      continue
    line = line[:-1]
    line = line.decode('utf-8')
    line = line.split(separator)
    callback(line, num)
    num += 1
