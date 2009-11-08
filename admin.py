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
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache

TEMPLATES_DIR = '%s/templates' % os.path.dirname(__file__)

def template_path(name):
  return os.path.join(TEMPLATES_DIR,'%s.tpl' % name)
  
class MainHandler(webapp.RequestHandler):
  def get(self):
		#template_data = {"page_title":"Home","session_user" : {"nickname":nickname},"tweets" : WFTweets}
		self.response.out.write(template.render(template_path(name='matrix'), None))
		
  def post(self):
    key_to_delete = self.request.get("memcache_key",default_value=None)
    logging.info('key_to_delete = %s' % key_to_delete)
    k = memcache.get(key_to_delete)
    logging.info('k = %s' % k)
    template_data = dict(key_to_delete=key_to_delete,key_value=k)
    self.response.out.write(template.render(template_path(name='matrix'), template_data))

class DeleteHandler(webapp.RequestHandler):
  def post(self,action):
    if action == 'key':
      del_key = self.request.get("del_key")
      try:
        memcache.delete(key=del_key)
        self.redirect('/matrix')
      except:
        self.error(500)
        self.response.out.write("delete from memcache didn't work")
    elif action == 'all':
      try:
        memcache.flush_all()
        self.redirect('/matrix')
      except:
        self.error(500)
        self.response.out.write("flush_all from memcache didn't work")
      
def main():
  urls = [
    ('/matrix/delete/(key|all)', DeleteHandler),
    ('/matrix', MainHandler)
    ]
  application = webapp.WSGIApplication(urls,debug=settings.debug)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
