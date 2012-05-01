# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from models import SieuxYonh, CjengMux, YonhMux, YonhMiukDzip, CjengLyih

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

def cjeng_mux_list_page(request):
  return render_to_response('kyonh/cjeng_mux_list.html', {
    'cjeng_mux_list': CjengMux.objects.all(),
  })

def yonh_mux_list_page(request):
  return render_to_response('kyonh/yonh_mux_list.html', {
    'yonh_mux_list': YonhMux.objects.get_pairs(),
  })

def yonh_miuk_list_page(request):
  return render_to_response('kyonh/yonh_miuk_list.html', {
    'yonh_miuk_list': YonhMiukDzip.objects.all(),
  })

def cjeng_ngix_list_page(request):
  return render_to_response('kyonh/cjeng_ngix_list.html', {
    'cjeng_mux_list': CjengMux.objects.all(),
  })

def yonh_ngix_list_page(request):
  return render_to_response('kyonh/yonh_ngix_list.html', {
    'yonh_mux_list': YonhMux.objects.get_pairs(),
  })

def yonh_do_page(request):
  page = int(request.GET.get('page', '1'))
  paginator = Paginator(YonhMiukDzip.objects.all(), 1)
  try:
    dzip_list = paginator.page(page)
  except (EmptyPage, InvalidPage):
    raise Http404()

  dzip = dzip_list[0]
  yonh_do = SieuxYonh.objects.get_yonh_do(dzip)

  return render_to_response('kyonh/yonh_do.html', {
    'yonh_do': yonh_do,
    'cjeng_lyih_list': CjengLyih.objects.all(),
    'dzip': dzip,
    'dzip_list': dzip_list,
  })
