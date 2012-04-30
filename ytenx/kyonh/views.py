# coding=utf-8
from django.shortcuts import render_to_response
from models import SieuxYonh

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
