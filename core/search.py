#!/usr/bin/env python
# encoding: utf-8
"""
search.py

Created by tim bart on 2009-10-31.
Copyright (c) 2009 Pims. All rights reserved.
"""
from utils import MemRedis
from utils import stopwords
from utils.twitter import TwitterAPI

import settings

import codecs
import logging
import os

try:
  from django.utils import simplejson
except:
  import simplejson

from time import sleep

def run(q):
  
  final_res = []
  r = MemRedis()
  
  w = [word.lower() for word in q.split() if word[0] != '-']
  dw = [word.lower() for word in q.split() if word[0] == '-']
  u = [word.lower() for word in q.split() if word[0] == '+']

  res_want = []
  res_dwant = []
  res_union = []
  for i in w:
    results = r.get('word|%s' % i)
    if results is not None:
      res_want +=  results

  for i in dw:
    results = r.get('word|%s' % i[1:])
    if results is not None:
      res_dwant +=  results

  for i in u:
    results = r.get('word|%s' % i[1:])
    if results is not None:
      res_union +=  results
      
  if len(res_want) > 0:
    want = set(res_want)
    dwant = set(res_dwant)
    union = set(res_union)
    
    res = want  - dwant
    if len(union) > 0:
      res = res.intersection(union)
    if len(res) == 0:
      return []
    else:
      
      for tweet_id in res:
        db_entry = r.get("id|%s" % tweet_id)
        if db_entry is not None:
          favorited_by = r.get("id|%s|fby" % tweet_id)
          text,screen_name,created_at = db_entry.split('|')
          mini_tweet = dict(id=tweet_id,text=text,screen_name=screen_name,created_at=created_at,favorited_by=favorited_by)
          final_res.append(mini_tweet)
  return final_res

def main():
	pass

if __name__ == '__main__':
	main()

