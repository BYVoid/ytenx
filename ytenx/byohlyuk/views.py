# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.paginator import InvalidPage, EmptyPage
from django.template.base import TemplateDoesNotExist
from ytenx.helpers.paginator import Paginator

def byoh_lyuk(request, name):
  if name == 'KienxPyan':
    return kienx_pyan()

  if not name:
    name = 'miuk_lyuk'
  
  path = 'byohlyuk/' + name + '.html'
  try:
    return render_to_response(path)
  except TemplateDoesNotExist:
    raise Http404()

def kienx_pyan():
  kienx_pyan_pieux = []
  for line in open('ytenx/byohlyuk/st_multi.txt'):
    line = line[:-1]
    line = line.decode('utf-8')
    line = line.split('\t')
    kienx_pyan_pieux.append(line)

  return render_to_response('byohlyuk/KienxPyan.html', {
    'kienx_pyan_pieux': kienx_pyan_pieux,
  })
