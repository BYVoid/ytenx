# coding=utf-8
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import SieuxYonh, YonhMux

def index_page(request):
  return render_to_response('kyonh/index.html')

def intro_page(request):
  return render_to_response('kyonh/intro.html')

def sieux_yonh_page(request, ziox):
  try:
    sieux_yonh = SieuxYonh.objects.get(ziox=ziox)
  except:
    raise Http404()

  return render_to_response('kyonh/sieux_yonh.html', {
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
  return render_to_response('kyonh/sieux_yonh_list.html', {
    'sieux_yonh_list': sieux_yonh_list,
  })

def yonh_mux_list_page(request):
  return render_to_response('kyonh/yonh_mux_list.html', {
    'yonh_mux_list': YonhMux.objects.get_pairs(),
  })
