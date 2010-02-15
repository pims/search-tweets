#!/usr/bin/env python
# encoding: utf-8

from core import bo
from utils import stopwords
from utils.twitter import TwitterAPI

import settings

import logging
import os

from django.utils import simplejson
from time import sleep

def classify(s):
  s = s.lower()
  s = s.replace('|','')
  s = to_unicode_or_bust(s)
  chars = ['[',']','.','!','?',',','(',')','"','\'',':',u'…','&','-','~',u'“',u'”']
  while len(s) > 0 and s[0] in chars:
    s = s[1:]
  
  while len(s) >0 and s[len(s)-1] in chars:
    s = s[0:len(s)-1]
  
  if len(s) > 2 and s[-2:] == '\'s' or s[-2:] == u'’s':
    s = s[:-2]
  
  if len(s) > 0:
    return s
  else:
    return None
  
def fetch(user):
  api = TwitterAPI(settings.TWITTER_USER,settings.TWITTER_PASSWORD)
  twitter_user = api.show_user(user)
  favorites = []
  if twitter_user is not None:
    favorites += api.favorites(user)
  else:
    logging.info("twitter_user = None for %s" % user)
  return favorites

def extract_words(s):
  # use re.split('\W+',s) ?
  return [w for w in s.split()]

def to_unicode_or_bust(obj, encoding='utf-8'):
  if isinstance(obj, basestring):
    if not isinstance(obj, unicode):
      obj = unicode(obj, encoding)
  return obj

def extract_and_clean_words(s):
  words = []
  for word in extract_words(s):
    w = classify(word)
    if w not in stopwords and w is not None:
      words.append(w)
  return list(set(words))

def run(user):
  try:
    favorites = fetch(user)
    if len(favorites) > 0:
      for favorite in favorites:
        existing_tweet = bo.Tweet.get_by_key_name(str(favorite['id']))
        if existing_tweet is not None and user not in existing_tweet.favorited_by:
          logging.info('%s also favorited tweet %s' % (user,favorite['id']))
          existing_tweet.favorited_by.append(user)
        else:
          word_log = False
          words = extract_and_clean_words(favorite['text'])
          tweet = bo.Tweet(
            key_name = str(favorite['id']),
            id = favorite['id'],
            text = favorite['text'],
            keywords = words,
            user = favorite["user"]["screen_name"],
            user_id = favorite["user"]["id"],
            favorited_by = [user]
          )
          tweet.put()
    return True
  except:
    raise
    logging.error('tweet %s not properly indexed' % favorite["id"])
    return False

def main():
	print classify('“I say fuck the odds, we are doing it.” — @felixge #hellyeah')

if __name__ == '__main__':
	main()

