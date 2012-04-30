# coding=utf-8
from django.shortcuts import render_to_response

def index_page(request):
  return render_to_response('kyonh/index.html')

def intro_page(request):
  return render_to_response('kyonh/intro.html')