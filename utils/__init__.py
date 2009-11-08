#!/usr/bin/env python
# encoding: utf-8
from google.appengine.api import memcache
import logging
import os

class Redis(object):
    data = {}
    def __init__(self):
        pass
 
    def get(self,key):
        if key in self.data:
            return self.data[key]
        else:
            return None

    def put(self,key,value):
        if key not in self.data:
            self.data[key] = value
            return True

    def push(self,key,value,tail=True):
        if key in self.data and type(self.data[key]) == list:
            if tail:
                if type(value) == list:
                    self.data[key] = self.data[key] + value
                else:
                    self.data[key].append(value)
                return True
            else:
                self.data[key] = [value,self.data[key][0:]]
        elif key not in self.data:
            self.data[key] = [value]
        else:
            return False

    def get_all(self,keys_only=False):
        res = []
        for key,item in self.data.iteritems():
          if keys_only:
            res.append(key)
          else:
            res.append((key,item))
        return res

class MemRedis():
  def __init__(self):
    pass
  
  def get(self,key):
    return memcache.get(key)

  def put(self,key,value):
    memcache.set(key,value)
    return True
  
  def push(self,key,value,tail=True):
    k = self.get(key)
    if k is not None and type(k) == list:
      if tail:
        if type(value) == list:
            self.put(key,k + value)
        else:
          k.append(value)
          self.put(key,k)
      else:
        if type(value) == list:
            self.put(key,k + value)
        else:
          self.put(key,[value,k[0:]])
    elif k is None:
      if type(value) == list:
        self.put(key,value)
      else:
        self.put(key,[value])
  
  def delete(self,key):
    memcache.delete(key)
    return True
  
  def flush_all(self):
    memcache.flush_all()
    return True

stopwords = ['a','about','above','across','after','again','against','all','almost','alone','along','already','also','although','always','among','an','and','another','any','anybody','anyone','anything','anywhere','are','area','areas','around','as','ask','asked','asking','asks','at','away','b','back','backed','backing','backs','be','became','because','become','becomes','been','before','began','behind','being','beings','best','better','between','big','both','but','by','c','came','can','cannot','case','cases','certain','certainly','clear','clearly','come','could','d','did','differ','different','differently','do','does','done','down','down','downed','downing','downs','during','e','each','early','either','end','ended','ending','ends','enough','even','evenly','ever','every','everybody','everyone','everything','everywhere','f','face','faces','fact','facts','far','felt','few','find','finds','first','for','four','from','full','fully','further','furthered','furthering','furthers','g','gave','general','generally','get','gets','give','given','gives','go','going','good','goods','got','great','greater','greatest','group','grouped','grouping','groups','h','had','has','have','having','he','her','here','herself','high','high','high','higher','highest','him','himself','his','how','however','i','if','important','in','interest','interested','interesting','interests','into','is','it','its','itself','j','just','k','keep','keeps','kind','knew','know','known','knows','l','large','largely','last','later','latest','least','less','let','lets','like','likely','long','longer','longest','m','made','make','making','man','many','may','me','member','members','men','might','more','most','mostly','mr','mrs','much','must','my','myself','n','necessary','need','needed','needing','needs','never','new','new','newer','newest','next','no','nobody','non','noone','not','nothing','now','nowhere','number','numbers','o','of','off','often','old','older','oldest','on','once','one','only','open','opened','opening','opens','or','order','ordered','ordering','orders','other','others','our','out','over','p','part','parted','parting','parts','per','perhaps','place','places','point','pointed','pointing','points','possible','present','presented','presenting','presents','problem','problems','put','puts','q','quite','r','rather','really','right','right','room','rooms','s','said','same','saw','say','says','second','seconds','see','seem','seemed','seeming','seems','sees','several','shall','she','should','show','showed','showing','shows','side','sides','since','small','smaller','smallest','so','some','somebody','someone','something','somewhere','state','states','still','still','such','sure','t','take','taken','than','that','the','their','them','then','there','therefore','these','they','thing','things','thinks','this','those','though','thought','thoughts','three','through','thus','to','today','together','too','took','toward','turn','turned','turning','turns','two','u','under','until','up','upon','us','use','used','uses','v','very','w','want','wanted','wanting','wants','was','way','ways','we','well','wells','went','were','what','when','where','whether','which','while','who','whole','whose','why','will','with','within','without','worked','working','works','would','x','y','year','years','yet','you','young','younger','youngest','your','yours','z']