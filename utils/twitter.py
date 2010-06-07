#!/usr/bin/env python
# encoding: utf-8
"""
twitter.py  

Created by tim bart on 2009-11-01.
Copyright (c) 2009 Pims. All rights reserved.
"""

import sys
import os
import urllib2
import logging

try:
  from django.utils import simplejson
except:
  import simplejson


class TwitterAPI(object):
  base_url = 'http://api.twitter.com/1'
  
  ratelimit_remaining = 150
  ratelimit_reset = 0
  
  current_user = (None,None)
  
  def __init__(self,user,password):
    self.user = user
    self.password = password
  
  def __handle_error(self,e):
    logging.info(e)
    return None
    
  def __fetch(self,url):
    headers = { 'User-Agent' : 'favorites fetcher 0.1 http://searchtweets.appspot.com' }
    full_url = self.base_url + url
    logging.info("Full url is : %s" % full_url)
    req = urllib2.Request(full_url, None, headers)
    try:
      response = urllib2.urlopen(req)
      return simplejson.loads(response.read())
    except urllib2.URLError, e:
      logging.error(e)
      return self.__handle_error(e)
  
  def favorites(self,user):
    __url = '/favorites/%s.json' % (user)
    favorites = self.__fetch(__url)
    if favorites is None:
      return []
    return favorites

def main():
  pass
  

if __name__ == '__main__':
  main()
