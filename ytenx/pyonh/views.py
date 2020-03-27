# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.db.models import Q
from ytenx.helpers.paginator import Paginator
from django.core.paginator import InvalidPage, EmptyPage
from ytenx.pyonh.models import CjengLyih, CjengMux, YonhBox, Dzih, SieuxYonh, Cio, YonhMux

def pyon_yonh(request):
  return render(request, 'pyonh/pyon_yonh.html', {
    'cjeng_mux_pieux': CjengLyih.objects.all(),
    'yonh_mux_pieux': YonhBox.objects.all(),
  })

def sieux_yonh(request, ziox):
  try:
    sieux_yonh = SieuxYonh.objects.get(ziox = ziox)
  except:
    raise Http404()

  return render(request, 'pyonh/sieux_yonh.html', {
    'sieux_yonh': sieux_yonh,
  })

def sieux_yonh_pieux(request):
  cjeng = request.GET.get('cjeng')
  yonh = request.GET.get('yonh')
  qim_jang = request.GET.get('qim_jang')
  deuh = request.GET.get('deuh')
  
  query = Q()
  if cjeng:
    query &= Q(cjeng = CjengMux.objects.get(dzih = cjeng))
  if yonh:
    query &= Q(yonh_box = YonhBox.objects.get(mjeng = yonh))
  if deuh:
    query &= Q(deuh = deuh)
  if qim_jang:
    query &= Q(qim_jang = qim_jang)
  
  sieux_yonh_pieux = SieuxYonh.objects.filter(query).order_by('ziox')
  paginator = Paginator(sieux_yonh_pieux, 15)
  try:
    sieux_yonh_pieux = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  
  sieux_yonh_pieux.cjeng = cjeng
  sieux_yonh_pieux.yonh = yonh
  sieux_yonh_pieux.deuh = deuh
  sieux_yonh_pieux.qim_jang = qim_jang
  
  cjeng_pieux = []
  for lyih in CjengLyih.objects.all():
    cjeng_pieux.append(lyih)
    cjeng_pieux += lyih.cjengmux_set.all()
  
  yonh_pieux = YonhBox.objects.all()
  
  return render(request, 'pyonh/sieux_yonh_pieux.html', {
    'sieux_yonh_pieux': sieux_yonh_pieux,
    'cjeng_pieux': cjeng_pieux,
    'yonh_pieux': yonh_pieux,
  })

def dzih(request, ziox):
  try:
    dzih = Dzih.objects.get(ziox=ziox)
  except:
    raise Http404()

  return render(request, 'pyonh/dzih.html', {
    'dzih': dzih,
  })

def dzih_pieux(request):
  dzih_pieux = Dzih.objects.all()
  paginator = Paginator(dzih_pieux, 15)
  try:
    dzih_pieux = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  return render(request, 'pyonh/dzih_pieux.html', {
    'dzih_pieux': dzih_pieux,
  })

@cache_page(60 * 60 * 24)
def cjeng_mux_pieux(request):
  return render(request, 'pyonh/cjeng_mux_pieux.html', {
    'cjeng_mux_pieux': CjengLyih.objects.all(),
  })

@cache_page(60 * 60 * 24)
def cjeng_mux(request, dzih):
  try:
    cjeng = CjengMux.objects.get(dzih = dzih)
  except:
    raise Http404()

  return render(request, 'pyonh/cjeng_mux.html', {
    'cjeng': cjeng,
  })

@cache_page(60 * 60 * 24)
def yonh_mux_pieux(request):
  return render(request, 'pyonh/yonh_mux_pieux.html', {
    'yonh_mux_pieux': YonhBox.objects.all(),
  })

@cache_page(60 * 60 * 24)
def yonh_mux(request, mjeng):
  try:
    yonh = YonhMux.objects.get(mjeng = mjeng)
  except:
    raise Http404()

  return render(request, 'pyonh/yonh_mux.html', {
    'yonh': yonh,
  })

def cio(request, kyenh, jep):
  cio = Cio.objects.get(
    kyenh = kyenh,
    jep = jep,
  )
  
  return render(request, 'pyonh/cio.html', {
    'cio': cio,
  })
