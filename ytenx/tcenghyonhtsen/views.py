# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from ytenx.helpers.paginator import Paginator
from django.core.paginator import InvalidPage, EmptyPage
from models import SieuxYonh, YonhBux, YonhMiuk, Cio

def index_page(request):
  return render(request, 'tcenghyonhtsen/index.html')

def sieux_yonh_page(request, ziox):
  try:
    sieux_yonh = SieuxYonh.objects.get(ziox=ziox)
  except:
    raise Http404()

  return render(request, 'tcenghyonhtsen/sieux_yonh.html', {
    'sieux_yonh': sieux_yonh,
  })

def sieux_yonh_list_page(request):
  sieux_yonh_list = SieuxYonh.objects.all().order_by('cioTriungZiox')
  paginator = Paginator(sieux_yonh_list, 15)
  try:
    sieux_yonh_list = paginator.page(request.GET)
  except (EmptyPage, InvalidPage):
    raise Http404()
  return render(request, 'tcenghyonhtsen/sieux_yonh_list.html', {
    'sieux_yonh_list': sieux_yonh_list,
  })

@cache_page(60 * 60 * 24)
def yonh_miuk_list_page(request):
  return render(request, 'tcenghyonhtsen/yonh_miuk_list.html', {
    'yonh_bux_list': YonhBux.objects.all(),
  })

def yonh_miuk_page(request, mjeng):
  yonh_miuk = YonhMiuk.objects.get(dzih = mjeng)

  return render(request, 'tcenghyonhtsen/yonh_miuk.html', {
    'yonh_miuk': yonh_miuk,
  })

def cio_page(request, kyenh, jep):
  cio = Cio.objects.get(
    kyenh = kyenh,
    jep = jep,
  )
  
  return render(request, 'tcenghyonhtsen/cio.html', {
    'cio': cio,
  })
