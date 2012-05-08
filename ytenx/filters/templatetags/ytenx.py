# coding:utf8
from django import template

register = template.Library()

num_map = {
  '1': u'一',
  '2': u'二',
  '3': u'三',
  '4': u'四',
  '5': u'五',
  '6': u'六',
  '7': u'七',
  '8': u'八',
  '9': u'九',
  '0': u'零',
  '10': u'十',
}

@register.filter
def sryoh(value):
  value = str(value)
  res = ''
  for i in range(0, len(value)):
    pos = len(value) - i
    c = value[i]
    res += num_map[c]
    if pos == 1 and c == '0' and len(value) > 1:
      res = res[:-1]
    if pos == 2:
      if c == '1':
        res = res[:-1]
      res += num_map['10']
  return res

@register.filter
def deuh(value):
  value = int(value)
  if value == 1: return u'平'
  if value == 2: return u'上'
  if value == 3: return u'去'
  if value == 4: return u'入'
  return value

@register.filter
def ho(value):
  if value: return u'開'
  return u'合'

@register.filter
def tshyuk(value):
  if value: return u'入'
  return u'舒'
