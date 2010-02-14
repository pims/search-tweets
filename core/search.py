#!/usr/bin/env python
# encoding: utf-8
"""
search.py

Created by tim bart on 2009-10-31.
Copyright (c) 2009 Pims. All rights reserved.
"""
from core import bo
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
  
  w = [word.lower() for word in q.split() if word[0] != '-']
  dw = [word.lower() for word in q.split() if word[0] == '-']
  u = [word.lower() for word in q.split() if word[0] == '+']

  res_want = []
  res_dwant = []
  res_union = []
  for i in w:
    results = bo.Tweet.all().filter('keywords =',i)
    for result in results:
      final_res.append(result)
  
  return final_res

def main():
	pass

if __name__ == '__main__':
	main()

