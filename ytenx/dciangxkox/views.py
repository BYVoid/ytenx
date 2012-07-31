# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.db.models import Q
from ytenx.helpers.paginator import Paginator
from django.core.paginator import InvalidPage, EmptyPage
from models import *

def triung_ngyan_qim_yonh(request):
  return render_to_response('dciangx/dciangx_kox.html')

def dzih(request, ziox):
  try:
    sieux_yonh = SieuxYonh.objects.get(ziox = ziox)
  except:
    raise Http404()

  return render_to_response('dciangx/sieux_yonh.html', {
    'sieux_yonh': sieux_yonh,
  })

def dzih_pieux(request):
  cjeng = request.GET.get('cjeng')
  yonh = request.GET.get('yonh')
  ho = request.GET.get('ho')
  deuh = request.GET.get('deuh')
  
  query = Q()
  if cjeng:
    query &= Q(cjeng = CjengMux.objects.get(dzih = cjeng))
  if yonh:
    query &= Q(yonh_box = YonhBox.objects.get(mjeng = yonh))
  if deuh:
    query &= Q(deuh = deuh)
  if ho:
    query &= Q(ho = ho)
  
  sieux_yonh_pieux = SieuxYonh.objects.filter(query).order_by('ziox')
  paginator = Paginator(sieux_yonh_pieux, 15)
  try:
    sieux_yonh_pieux = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  
  sieux_yonh_pieux.cjeng = cjeng
  sieux_yonh_pieux.yonh = yonh
  sieux_yonh_pieux.deuh = deuh
  sieux_yonh_pieux.ho = ho
  
  cjeng_pieux = []
  for lyih in CjengLyih.objects.all():
    cjeng_pieux.append(lyih)
    cjeng_pieux += lyih.cjengmux_set.all()
  
  yonh_pieux = YonhBox.objects.all()
  
  return render_to_response('dciangx/sieux_yonh_pieux.html', {
    'sieux_yonh_pieux': sieux_yonh_pieux,
    'cjeng_pieux': cjeng_pieux,
    'yonh_pieux': yonh_pieux,
  })

#@cache_page
def cjeng_byo_pieux(request):
  return render_to_response('dciangx/cjeng_mux_pieux.html', {
    'cjeng_mux_pieux': CjengLyih.objects.all(),
  })

#@cache_page
def cjeng_byo(request, dzih):
  try:
    cjeng = CjengMux.objects.get(dzih = dzih)
  except:
    raise Http404()

  return render_to_response('dciangx/cjeng_mux.html', {
    'cjeng': cjeng,
  })

#@cache_page
def yonh_box_pieux(request):
  return render_to_response('dciangx/yonh_mux_pieux.html', {
    'yonh_mux_pieux': YonhBox.objects.all(),
  })

#@cache_page
def yonh_box(request, mjeng):
  try:
    yonh = YonhMux.objects.get(mjeng = mjeng)
  except:
    raise Http404()

  return render_to_response('dciangx/yonh_mux.html', {
    'yonh': yonh,
  })
