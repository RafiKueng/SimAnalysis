# -*- coding: utf-8 -*-
"""

perfect analysis script

1. fetches the modelled sims from the thread and gets their id
2. increases the pixrad and lets the models run again
3. creates nice output logs, list of ids for the analysis.py script and a posting for the forum

Created on Tue Aug 15 12:05:31 2013

@author: RafiK
"""

debug = True
dryrun = True

import requests as rq
import math
import re
import string

copydict = lambda dct, *keys: {key: dct[key] for key in keys}

rid_re = re.compile('mite\.physik\.uzh\.ch\/data\/(\d+)(.*?)(\n|$|http)')
punct1_re = re.compile('^\s*[{0}]\s*[{0}]*'.format(re.escape(string.punctuation)))
punct2_re = re.compile('\s*[{0}]*\s*[{0}]+\s*$'.format(re.escape(string.punctuation)))
swid_re = re.compile('ASW000....')
auth_re = re.compile('meta\(author=\'(.*)\',')
inf_re = re.compile('globject\(\'(\d+)__(.+)\'')
nmod_re = re.compile('model\((\d+)')

id_re = re.compile('Result for (ASW000....)')
pxr_re = re.compile('Pixel Radius:</span>(\d+)')
nmod_re = re.compile('Nr of models:</span>(\d+)')
rusr_re = re.compile('User:</span>(.*?)</li>')


class GetOutOfLoop( Exception ):
  pass


def getLenses():
  
  board_id = "BSW0000006"
  disc_id = "DSW00007j5"
  
  url = "https://api.zooniverse.org/projects/spacewarp/talk/boards/%s/discussions/%s"
  
  
  se = rq.session()
  se2 = rq.session()
  resp = se.get(url % (board_id, disc_id))
  jresp = resp.json()
  n_com = jresp['comments_count']
  n_pages = int(math.ceil(n_com / 10.))
  
  comments = []
  users = {}
  lenses = {}
  
  for i in range(n_pages):
    comments.extend(se.get((url % (board_id, disc_id)) + '/comments?page=' + str(i+1)).json())
    
  try:
    for i, comment in enumerate(comments):
      txt = comment['body']
      user = copydict(comment, 'user_name', 'user_id', 'user_zooniverse_id')
      user['alias'] = [comment['user_name']]
      users[user["user_name"]] = user
      rids = rid_re.findall(comment['body'])
      
      
      for rid, com, _ in rids:
        com = swid_re.sub('', com) # remove spacewarps ids
        com = punct1_re.sub('', com) # remove punctuation chars at start
        #com = punct2_re.sub('', com) # remove punctuation chars at end
        com = com.strip() #remove trailing whitechars
        
        txt = se2.get("http://mite.physik.uzh.ch/data/%s" % rid).content
        swid = id_re.search(txt).groups()[0]
        pxr  = pxr_re.search(txt).groups()[0]
        nmod = nmod_re.search(txt).groups()[0]
        rusr = rusr_re.search(txt).groups()[0]
        
        if rusr not in user['alias']:
          user['alias'].append(rusr)
        users[rusr] = user
        
        model = {
          'id': rid,
          'user': user,
          'pxr': pxr,
          'nmod': nmod,
          'com': com, #comment
          }
  
        print rid, swid, pxr, nmod, rusr, com
        
        if swid in lenses:
          lenses[swid].append(model)
        else:
          lenses[swid] = [model]
        
              
  
  except GetOutOfLoop:
    pass
  
  
  print "Overview"
  for swid, models in lenses.items():
    print '  Possible models for ' + swid
    for model in models:
      print "    {id}: by: {user[user_name]:12} p:{pxr:2} m:{nmod:4}) comment: {com}".format(**model)
  
  return lenses  


#for debug

if debug:
  user = {'user_name': u'Demouser'}
  model = {
      'pxr': '6',
      'com': u"I can't make this one  look good.",
      'id': u'000120',
      'nmod': '200',
      'user': user,
    }
  
  lenses = {'ASW0002kjj': [model, model], 'ASW0002kji': [model, model], }
else:
  lenses = getLenses()



# create new better models
###############################

import os, shutil

from ModellerApp.models import ModellingResult
from lmt.tasks import calculateModel
from django.utils import timezone
#from celery.result import AsyncResult

#increasing pixel range
new_pxr = 12
new_nmod = 200

if debug:
  logdir = './'
else:
  logdir = '/tmp/lmt/'
  os.mkdir(logdir)

logf  = open(logdir+'log.txt', 'w')
newids= open(logdir+'ids.txt', 'w')
post  = open(logdir+'post.txt', 'w')

for swid, models in lenses.items():
  print '  Possible models for ' + swid
  logf.write(swid+'\n')
  post.write("\nSim ID: {0}\n\n".format(swid))
  for model in models:
    print "    {id}: by: {user[user_name]:12} p:{pxr:2} m:{nmod:4} comment: '{com}'".format(**model) ,

    # find model in db
    try:
      mresobj_old = ModellingResult.objects.get(id=model['id'])
      mresobj_new = ModellingResult.objects.get(id=model['id'])
    except ModellingResult.DoesNotExist:
      print "ERROR, model not found"
      continue
    mresobj_new.pk = None #This copies the original one!!
    mresobj_new.save()
    mresobj_new.parent_result = mresobj_old
    mresobj_new.created_by_str = mresobj_new.created_by_str + ' [enh]'
    mresobj_new.created = mresobj_new.created
    mresobj_new.rendered_last = timezone.now()
    mresobj_new.pixrad = new_pxr
    mresobj_new.n_models = new_nmod
    mresobj_new.is_rendered = True
    mresobj_new.save()
    new_id = mresobj_new.pk
    #print new_id

    datapath =   '../tmp_media/%06i' % mresobj_new.pk
    old_datapath =   '../tmp_media/%06i' % mresobj_old.pk
    
    os.mkdir(datapath)
    #shutil.copy(old_datapath+'/cfg.gls', datapath+'/cfg.gls')
    try:
      shutil.copy(old_datapath+'/input.png', datapath+'/input.png')
    except:
      pass
    
    with open(old_datapath+'/cfg.gls', 'r') as f:
      txt = f.read()
    with open(datapath+'/cfg.gls', 'w') as f:
      txt = re.sub('pixrad\((\d+)\)', "pixrad(%i) #man"%new_pxr, txt)
      txt = re.sub('model\((\d+)\)', "model(%i) #man"%new_nmod, txt)
      txt = re.sub('tmp_media/\d+', "tmp_media/%06i"%new_id, txt)
      f.write(txt)
      
    task = calculateModel.apply_async(args=(new_id,), timeout=10e10, expires=10e10)
    mresobj_new.task_id = task.task_id
    mresobj_new.save()
    
      
    print " --> improved_id: {0}".format(new_id)
    logf.write("  {id}: by: {user[user_name]:12} p:{pxr:2} m:{nmod:4} comment: '{com}'".format(**model))
    logf.write("  improved_id: {0}\n".format(new_id))
    logf.flush()
    post.write(" - [model {0:06}, was {1:06}](http://mite.physik.uzh.ch/data/{0:06}) | by: {2} | time: {3} | comment: '{4}'\n".format(
      new_id, mresobj_old.pk, mresobj_old.created_by_str, mresobj_old.created, model['com']
    ))
    post.flush()
    newids.write("%06i\n"%new_id)
    newids.flush()
    
    if dryrun: break
  if dryrun: break
    
logf.close()
post.close()
newids.close()
