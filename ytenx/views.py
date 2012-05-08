# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response

def index_page(request):
  return render_to_response('index.html')

def about_page(request):
  return render_to_response('about.html')
