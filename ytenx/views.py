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
  dzih = request.GET.get('dzih')
  
  dzih_list = {
    'kyonh': KyonhDzih.objects.filter(dzih = dzih),
    'tcyts': TcytsDzih.objects.filter(dzih = dzih),
  }
  
  return render_to_response('zim.html', {
    'dzih_list': dzih_list,
  })
