# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import SieuxYonh, YonhBux, YonhMiuk, Cio

def index_page(request):
  return render_to_response('tcenghyonhtsen/index.html')

def sieux_yonh_page(request, ziox):
  try:
    sieux_yonh = SieuxYonh.objects.get(ziox=ziox)
  except:
    raise Http404()

  return render_to_response('tcenghyonhtsen/sieux_yonh.html', {
    'sieux_yonh': sieux_yonh,
  })

def sieux_yonh_list_page(request):
  sieux_yonh_list = SieuxYonh.objects.all()
  page = int(request.GET.get('page', '1'))
  paginator = Paginator(sieux_yonh_list, 15)
  try:
    sieux_yonh_list = paginator.page(page)
  except (EmptyPage, InvalidPage):
    raise Http404()
  return render_to_response('tcenghyonhtsen/sieux_yonh_list.html', {
    'sieux_yonh_list': sieux_yonh_list,
  })

def yonh_miuk_list_page(request):
  return render_to_response('tcenghyonhtsen/yonh_miuk_list.html', {
    'yonh_bux_list': YonhBux.objects.all(),
  })

def yonh_miuk_page(request, mjeng):
  yonh_miuk = YonhMiuk.objects.get(dzih = mjeng)

  return render_to_response('tcenghyonhtsen/yonh_miuk.html', {
    'yonh_miuk': yonh_miuk,
  })

def cio_page(request, kyenh, jep):
  cio = Cio.objects.get(
    kyenh = kyenh,
    jep = jep,
  )
  
  return render_to_response('tcenghyonhtsen/cio.html', {
    'cio': cio,
  })
