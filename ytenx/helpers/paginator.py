# coding=utf-8
from django.core.paginator import Paginator as DjangoPaginator, Page as DjangoPage

class Page(DjangoPage):
  def __init__(self, page, req):
    DjangoPage.__init__(self, page.object_list, page.number, page.paginator)
    self.req = req

  def args(self, page):
    self.req['page'] = page
    arglist = []
    for key, value in self.req.items():
      if value:
        arglist.append('%s=%s' % (key, value))
    
    arguments = '&'.join(arglist)
    return arguments
  
  def args_first(self):
    return self.args(1)
  
  def args_second(self):
    return self.args(2)
    
  def args_last(self):
    return self.args(self.paginator.num_pages)
    
  def args_current(self):
    return self.args(self.number)
  
  def args_previous(self):
    return self.args(self.previous_page_number())
  
  def args_next(self):
    return self.args(self.next_page_number())

class Paginator(DjangoPaginator):
  def page(self, rawreq):
    req = {}
    for key, value in rawreq.items():
      req[key] = value
    return Page(DjangoPaginator.page(self, req.get('page', '1')), req)
