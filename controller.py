#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import wsgiref.handlers
import os

import settings

from utils import stopwords
from utils import MemRedis

from core import search
from core import index

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

TEMPLATES_DIR = '%s/templates' % os.path.dirname(__file__)

def template_path(name):
  return os.path.join(TEMPLATES_DIR,'%s.tpl' % name)
  
class MainHandler(webapp.RequestHandler):
  def get(self):
		template_data = dict(analytics=settings.analytics)
		self.response.out.write(template.render(template_path(name='home'), template_data))

class SearchHandler(webapp.RequestHandler):
  def get(self):
    q = self.request.get("q")
    results = []
    error = None
    if q not in stopwords:
      results = search.run(q)
    else:
      error = u'the word you searched for isn\'t currently indexed, we think it doesn\'t make much sense, @pims if you think we should totally index it !'
    
    template_data = {"page_title":"Home","results" : results,"error":error,"analytics":settings.analytics}
    self.response.out.write(template.render(template_path(name='results'), template_data))

class IndexHandler(webapp.RequestHandler):
  def get(self,username):
    if self.request.get("token") == settings.index_token:
      if index.run(username):
        self.redirect('/')
      else:
        self.error(500)
        self.response.out.write("error while indexing")
    else:
      self.error(404)
      self.response.out.write("page not found :(")
      
  def post(self,code):
    if code != '333':
      self.error(400)
      self.response.out.write("Bad Request moron")
    else:
      data = self.request.get("data")
      username = self.request.get("username")
      search.index(username,data=data)
      self.response.out.write("yippie")
def main():
  urls = [
    ('/search',SearchHandler),
    ('/', MainHandler),
    ('/index/(.*)',IndexHandler)
    ]
  application = webapp.WSGIApplication(urls,debug=settings.debug)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
