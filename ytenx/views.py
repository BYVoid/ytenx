# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from jihthex.models import Dzih as JihThex
from kyonh.models import Dzih as KyonhDzih
from tcenghyonhtsen.models import Dzih as TcytsDzih
from pyonh.models import Dzih as PyonhDzih
from trngyan.models import Dzih as TrngyanDzih

def index_page(request):
  return render_to_response('index.html')

def about_page(request):
  return render_to_response('about.html')

def kiemx_sriek(request):
  return render_to_response('kiemx_sriek.html')

def zim(request):
  chom_sryoh = {
    'dzih_pieux': request.GET.get('dzih', ''),
    'zim_kyonh': request.GET.get('kyonh'),
    'zim_trngyan': request.GET.get('trngyan'),
    'zim_tcyts': request.GET.get('tcyts'),
    'zim_pyonh': request.GET.get('pyonh'),
    'jih_thex_dzyen_tongx': request.GET.get('jtdt'),
    'jih_thex_krau_dep': request.GET.get('jtkd'),
    'jih_thex_krenx_byan': request.GET.get('jtkb'),
  }
  
  if request.GET.get('dzyen'):
    chom_sryoh['zim_kyonh'] = True
    chom_sryoh['zim_trngyan'] = True
    chom_sryoh['zim_tcyts'] = True
    chom_sryoh['zim_pyonh'] = True
  
  if len(chom_sryoh['dzih_pieux']) > 5:
    chom_sryoh['dzih_pieux'] = chom_sryoh['dzih_pieux'][0:5]
  
  dzih_liet = {}
  for dzih in chom_sryoh['dzih_pieux']:
    dzih_liet[dzih] = True
    #轉換異體
    if chom_sryoh['jih_thex_dzyen_tongx'] or chom_sryoh['jih_thex_krau_dep'] or chom_sryoh['jih_thex_krenx_byan']:
      jih_thex = JihThex.objects.filter(dzih = dzih)
      if jih_thex:
        assert(len(jih_thex) == 1)
        jih_thex = jih_thex[0]
        #全等異體
        if chom_sryoh['jih_thex_dzyen_tongx']:
          for dzih in jih_thex.dzyen_tongx.all():
            dzih_liet[dzih.dzih] = True
        #語義交疊異體
        if chom_sryoh['jih_thex_krau_dep']:
          for dzih in jih_thex.krau_dep.all():
            dzih_liet[dzih.dzih] = True
        #簡繁
        if chom_sryoh['jih_thex_krenx_byan']:
          for dzih in jih_thex.byan.all():
            dzih_liet[dzih.dzih] = True
  dzih_liet = dzih_liet.keys()
  
  dzih_list = {}
  if chom_sryoh['zim_kyonh']:
    dzih_list['kyonh'] = KyonhDzih.objects.filter(dzih__in = dzih_liet).order_by('ziox')
  if chom_sryoh['zim_tcyts']:
    dzih_list['tcyts'] = TcytsDzih.objects.filter(dzih__in = dzih_liet).order_by('ziox')
  if chom_sryoh['zim_pyonh']:
    dzih_list['pyonh'] = PyonhDzih.objects.filter(dzih__in = dzih_liet).order_by('ziox')
  if chom_sryoh['zim_trngyan']:
    dzih_list['trngyan'] = TrngyanDzih.objects.filter(dzih__in = dzih_liet).order_by('ziox')
  
  return render_to_response('zim.html', {
    'dzih_list': dzih_list,
    'chom_sryoh': chom_sryoh,
  })
