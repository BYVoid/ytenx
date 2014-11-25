# coding=utf-8
from common import traverse
from django.http import HttpResponse
from ytenx.jihthex.models import *

basePath = './ytenx/sync/jihthex/'
dzih_map = {}

def sync():
  syncDzih()
  print 'Jihthex Done'

def syncDzih():
  
  def sync_dzih(line, num):
    dzih = Dzih(
      dzih = line[0]
    )
    dzih.save()
    dzih_map[dzih.dzih] = dzih  
    
  def sync_kruan(line, num):
    dzih = dzih_map[line[0]]
    for c in line[1]:
      dzih.dzyen_tongx.add(c)
    for c in line[2]:
      dzih.krau_dep.add(c)
    for c in line[3]:
      dzih.krenx.add(c)
    for c in line[4]:
      dzih.byan.add(c)
    dzih.save()
  
  print 'Dzih...'
  traverse(basePath + 'JihThex.csv', sync_dzih, separator=',')
  print 'Done'
  print 'DzihKruan...'
  traverse(basePath + 'JihThex.csv', sync_kruan, separator=',')
  print 'Done'
