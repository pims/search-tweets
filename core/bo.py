#!/usr/bin/env python
# encoding: utf-8

from google.appengine.ext import db

class Tweet(db.Model):
  id = db.IntegerProperty()  
  text = db.TextProperty()
  keywords = db.StringListProperty()
  favorited_by = db.StringListProperty()
  user = db.StringProperty()
  user_id = db.IntegerProperty()
  indexed_date = db.DateTimeProperty(auto_now_add=True)