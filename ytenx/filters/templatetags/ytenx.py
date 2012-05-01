# coding:utf8
from django import template

register = template.Library()

@register.filter
def sryoh(value):
  value = str(value)
  value = value.replace('1', u'一')
  value = value.replace('2', u'二')
  value = value.replace('3', u'三')
  value = value.replace('4', u'四')
  value = value.replace('5', u'五')
  value = value.replace('6', u'六')
  value = value.replace('7', u'七')
  value = value.replace('8', u'八')
  value = value.replace('9', u'九')
  value = value.replace('0', u'零')
  return value

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
