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
  '100': u'百',
  '1000': u'千',
}

@register.filter
def sryoh(value):
  value = str(value)
  res = ''
  length = len(value)
  for i in range(0, length):
    pos = len(value) - i
    c = value[i]
    res += num_map[c] #當前數字位
    if pos == 1:
      pass
    elif pos == 2:
      if c == '1' and length == 2: #變「一十」爲「十」
        res = res[:-1]
      if c != '0':
        res += num_map['10']
    elif pos == 3:
      if c != '0':
        res += num_map['100']
    elif pos == 4:
      if c != '0':
        res += num_map['1000']
  if length > 1:
    while res[-1] == num_map['0']:
      res = res[:-1]
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
def deuh_trngyan(value):
  value = int(value)
  if value == 1: return u'陰平'
  if value == 2: return u'陽平'
  if value == 3: return u'上聲'
  if value == 4: return u'去聲'
  if value == 5: return u'入聲作平聲'
  if value == 6: return u'入聲作上聲'
  if value == 7: return u'入聲作去聲'
  return value

@register.filter
def ho(value):
  if value: return u'開'
  return u'合'

@register.filter
def tshyuk(value):
  if value: return u'入'
  return u'舒'

@register.filter
def qim_jang(value):
  if value: return u'陽'
  return u'陰'

@register.filter
def dciangx_ghrax(value):
  value = int(value)
  if value == 1: return u'上'
  return u'下'

@register.filter
def siih_ho(value):
  value = int(value)
  if value == 1: return u'開口呼'
  if value == 2: return u'合口呼'
  if value == 3: return u'齊齒呼'
  if value == 4: return u'撮口呼'
  return value

@register.filter
def krak_cik(text):
  return text.replace(r'\n', "<br>")

@register.filter
def neom_khiowk(text):
  result = text
  result = result.replace(r'yut', "yʔ")
  return text
