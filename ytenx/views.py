# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from kyonh.models import Dzih as KyonhDzih
from tcenghyonhtsen.models import Dzih as TcytsDzih

def index_page(request):
  return render_to_response('index.html')

def about_page(request):
  return render_to_response('about.html')

def zim(request):
  dzih_pieux = request.GET.get('dzih')
  
  if not dzih_pieux:
    dzih_pieux = ''
  
  if len(dzih_pieux) > 8:
    dzih_pieux = dzih_pieux[0:8]
  
  dzih_liet = []
  for dzih in dzih_pieux:
    dzih_liet.append(dzih)
  
  dzih_list = {}
  zim_kyonh = request.GET.get('kyonh')
  zim_tcyts = request.GET.get('tcyts')
  
  if zim_kyonh:
    dzih_list['kyonh'] = KyonhDzih.objects.filter(dzih__in = dzih_liet).order_by('ziox')
  if zim_tcyts:
    dzih_list['tcyts'] = TcytsDzih.objects.filter(dzih__in = dzih_liet).order_by('ziox')
  
  return render_to_response('zim.html', {
    'dzih_list': dzih_list,
  })
