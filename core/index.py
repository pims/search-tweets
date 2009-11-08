#!/usr/bin/env python
# encoding: utf-8

from utils import MemRedis
from utils import stopwords
from utils.twitter import TwitterAPI

import settings

import codecs
import logging
import os

from django.utils import simplejson
from time import sleep

def classify(s):
  s = s.lower()
  s = s.replace('|','')
  s.encode("utf-8")
  chars = ['[',']','.','!','?',',',',','(',')','"','\'',':',u'…']
  while len(s) > 0 and s[0] in chars:
    s = s[1:]
  
  while len(s) >0 and s[len(s)-1] in chars:
    s = s[0:len(s)-1]
  
  if len(s) > 2 and s[-2:] == '\'s' or s[-2:] == u'’s':
    s = s[:-2]
  
  if len(s) > 0:
    return 'word|%s' % s
  else:
    return None

def load_data(user):
  files = []
  for f in os.listdir('static'):
    if f[-5:] == '.json':
      fh = codecs.open('static/' + f,'r','utf-8')
      content = fh.read()
      fh.close()
      files += simplejson.loads(content)
  return files
  
def fetch(user):
  api = TwitterAPI(settings.twitter_user,settings.twitter_password)
  twitter_user = api.show_user(user)
  favorites = []
  if twitter_user is not None:
    favorites += api.favorites(user)
  else:
    logging.info("twitter_user = None for %s" % user)
  return favorites
    
def run(user):
  properly_indexed = False
  r = MemRedis()
  #r.flush_all()
  if r.get('indexed|%s' % user) is None:
    
    favorites = fetch(user)
    if len(favorites) > 0:
      for favorite in favorites:
        
        #we don't want to reindex the whole content if tweet already in datastore
        if r.get("id|%s" % favorite["id"]) is None:
          r.put("id|%s" % favorite["id"],"%s|%s|%s" % (favorite["text"],favorite["user"]["screen_name"],favorite["created_at"]))
          r.push("id|%s|fby" % favorite["id"],str(user))
          
          #now we index “all” the words in that tweet
          for word in favorite["text"].split():
            if word not in stopwords and classify(word) is not None:
              r.push(classify(word),str(favorite["id"]))
        
        #popularity
        fav = r.get("id|%s|fby" % favorite["id"])
        if fav is None or user not in r.get("id|%s|fby" % favorite["id"]):
          r.push("id|%s|fby" % favorite["id"],str(user))
      
      r.put('indexed|%s' % user,1)
      properly_indexed = True
    else:
      logging.info("%s empty favorite" % user)
  else:
    logging.info("%s already indexed" % user)
  
  return properly_indexed

def main():
	pass

if __name__ == '__main__':
	main()

