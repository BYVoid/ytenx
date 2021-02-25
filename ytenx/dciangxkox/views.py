# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.db.models import Q
from ytenx.helpers.paginator import Paginator
from django.core.paginator import InvalidPage, EmptyPage
from ytenx.dciangxkox.models import Dzih, CjengByo, YonhBox

def dciangx_kox(request):
  return render(request, 'dciangxkox/dciangx_kox.html')

def dzih(request, id):
  try:
    dzih = Dzih.objects.get(id = id)
  except:
    raise Http404()

  return render(request, 'dciangxkox/dzih.html', {
    'dzih': dzih,
  })

def dzih_pieux(request):
  yonh = request.GET.get('yonh')
  
  query = Q()
  if yonh:
    query &= Q(yonh = YonhBox.objects.get(mjeng = yonh))
  
  dzih_pieux = Dzih.objects.filter(query).order_by('ziox')
  paginator = Paginator(dzih_pieux, 15)
  try:
    dzih_pieux = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  
  dzih_pieux.yonh = yonh
  
  cjeng_pieux = CjengByo.objects.all()
  yonh_pieux = YonhBox.objects.all()
  
  return render(request, 'dciangxkox/dzih_pieux.html', {
    'dzih_pieux': dzih_pieux,
    'cjeng_pieux': cjeng_pieux,
    'yonh_pieux': yonh_pieux,
  })

@cache_page(60 * 60 * 24)
def cjeng_byo_pieux(request):
  cjeng_pieux = CjengByo.objects.all()
  paginator = Paginator(cjeng_pieux, 15)
  try:
    cjeng_pieux = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  
  return render(request, 'dciangxkox/cjeng_byo_pieux.html', {
    'cjeng_pieux': cjeng_pieux,
  })

@cache_page(60 * 60 * 24)
def cjeng_byo(request, mjeng):
  try:
    cjeng = CjengByo.objects.get(mjeng = mjeng)
  except:
    raise Http404()

  return render(request, 'dciangxkox/cjeng_byo.html', {
    'cjeng': cjeng,
  })

@cache_page(60 * 60 * 24)
def yonh_box_pieux(request):
  return render(request, 'dciangxkox/yonh_box_pieux.html', {
    'yonh_pieux': YonhBox.objects.all(),
  })

@cache_page(60 * 60 * 24)
def yonh_box(request, mjeng):
  try:
    yonh = YonhBox.objects.get(mjeng = mjeng)
  except:
    raise Http404()

  return render(request, 'dciangxkox/yonh_box.html', {
    'yonh': yonh,
  })
