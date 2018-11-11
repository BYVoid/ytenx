# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from ytenx.helpers.paginator import Paginator
from django.core.paginator import InvalidPage, EmptyPage
from models import SieuxYonh, YonhBux, YonhMiuk, Cio, QimBjin

def index_page(request):
  return render(request, 'tcenghyonhtsen/index.html')

def sieux_yonh_page(request, ziox):
  try:
    sieux_yonh = SieuxYonh.objects.get(ziox=ziox)
  except:
    raise Http404()
    
  qim_bjin_set = QimBjin.objects.filter(t1 = ziox) | QimBjin.objects.filter(t2 = ziox) | QimBjin.objects.filter(t3 = ziox) | QimBjin.objects.filter(t4 = ziox);
  qim_bjin_text = ''
  qim_bjin_filename = ''
  if qim_bjin_set.count() = 1:
    qim_bjin = qim_bjin_set[:1].get()
    qim_bjin_filename = qim_bjin.filename
    qim_bjin_text = u'平' + SieuxYonnh.objects.get(ziox = qim_bjin.t1).ipa
    if qim_bjin.merge_t2_t3:
      qim_bjin_text = qim_bjin_text + u' 上去'
      if qim_bjin.t3 != '?':
        qim_bjin_text = qim_bjin_text + qim_bjin.t3
      else:
        qim_bjin_text = qim_bjin_text + qim_bjin.t2
      else:
        qim_bjin_text = qim_bjin_text + u' 上' + qim_bjin.t2 + u' 去' + qim_bjin.t3
    if qim_bjin.t4 != ''
        qim_bjin_text = qim_bjin_text + u' 入' + qim_bjin.t4

  return render(request, 'tcenghyonhtsen/sieux_yonh.html', {
    'sieux_yonh': sieux_yonh,
    'qim_bjin_text': qim_bjin_text,
    'qim_bjin_filename': qim_bjin_filename
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
