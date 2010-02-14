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
  base_url = 'http://twitter.com'
  
  ratelimit_remaining = 150
  ratelimit_reset = 0
  
  current_user = (None,None)
  
  def __init__(self,user,password):
    self.user = user
    self.password = password
  
  def __handle_error(self,e):
    logging.info(e)
    return None
    
  def __fetch(self,url,format):
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, self.base_url,self.user,self.password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    try:
      req = opener.open(self.base_url + url)
      if format == 'json':
        return simplejson.loads(req.read())
      else:
        return req.read()
    except urllib2.URLError, e:
      logging.error(req.info())
      self.__handle_error(e)
    
  
  def show_user(self,user=None,format='json'):
    if user is None : user = self.user
    __url = '/users/show/%s.%s' % (user,format)
    twitter_user = self.__fetch(__url,format)
    self.current_user = (user,twitter_user)
    return twitter_user
  
  def favorites(self,user=None,format='json'):
    if user is None : user = self.user
    __url = '/favorites/%s.%s' % (user,format)
    favorites = []
    if user == self.current_user[0] and self.current_user[1]["favourites_count"] is not None:
      num_favorites = min(100,self.current_user[1]["favourites_count"])
      
      if num_favorites % 20 == 0:
        num_pages = num_favorites / 20
      else:
        num_pages = (num_favorites / 20) + 1
      for i in range(1,num_pages+1):
        url = "%s?page=%s" % (__url,i)
        part = self.__fetch(url,format)
        if part is not None and len(part) > 0:
          favorites += part
        else:
          break
      
    return favorites

def main():
  pass
  

if __name__ == '__main__':
  main()
