# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:18:42 2013

@author: rafik
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

#from matplotlib import rc

#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)


sims_dir = '../systems/figs'
user_data_dir = './data.csv'
save_fig_path = './figs'

div_scale_factors = 440./500*100

data = []

# read the user generated data
with open(user_data_dir, 'r') as f:

  c = 6 # offset for real data

  csvfile = csv.reader(f)
  
  for row in csvfile:
    l = len(row)

    dl = (l-c-int(row[4])*2) / 4  
    
    #print l, dl, (l-5-int(row[4])*2) % 4
    if (l-c-int(row[4])*2) % 4 != 0:
      print '!! strange2 error @', row[0]
      continue 
    
    points = []
    pntdata = row[c+4*dl:]
    for ii in range(int(row[4])):
      points.append({'d':float(pntdata[ii*2])*div_scale_factors,'t':pntdata[ii*2+1]})
      
    o = {
      'id':     int(row[0]),
      'user':   row[1],
      'name':   row[2],
      'nr':     int(row[3]),
      'pxR':    int(row[3])-1,
      'nPnt':   int(row[4]),
      'nMod':   int(row[5]),
      'x':      np.array(row[c:c+dl], dtype=np.float32),
      'y':      np.array(row[c+dl: c+2*dl], dtype=np.float32),
      'err_p':  np.array(row[c+2*dl: c+3*dl], dtype=np.float32),
      'err_m':  np.array(row[c+3*dl: c+4*dl], dtype=np.float32),
      'pnts' :  points
      }
    data.append(o)
      
      #[fl, author, name, len(x_vals)] + list(x_vals) + list(kappaRd_median) + list(kappaRenc_1sigmaplus) + list(kappaRenc_1sigmaminus))


#read the sims data
import glob
import os

paths = glob.glob(os.path.join(sims_dir, '*.txt' ))

sims = {}

for path in paths:
  with open(path, 'r') as f:
    lines = f.readlines()
    
    name = os.path.basename(path)[:-4] # strip .txt
    
    xvals = []
    yvals = []
    
    for line in lines:
      #print line
      try:    
        x, _, y = line.strip().split(' ')
      except:
        print 'split not possible' 
        continue
      xvals.append(x)
      yvals.append(y)
    
    vals = {
      'x': np.array(xvals, dtype=np.float32),
      'y': np.array(yvals, dtype=np.float32),
    }
    sims[name] = vals



# do the plots
def plott(idd, show=True, cenc=False):

  elem = data[idd]
  name = elem['name']

  try:
    sims[name]
  except KeyError:
    print '!! missing sims data for', idd, name
    return
    
    
  plt.ioff()
  
  fig = plt.figure()
  #panel = fig.add_subplot(1,1,1)
  
  
  yerr=[elem['err_p'] - elem['y'], elem['y']- elem['err_m']]

  #plt.errorbar(elem['x'], elem['y'], yerr=yerr)
  plt.plot(elem['x'], elem['err_p'], 'b')
  plt.plot(elem['x'], elem['err_m'], 'b')
  #plt.plot(elem['x'], elem['y'], 'k')
  plt.fill_between(elem['x'], elem['err_p'], elem['err_m'], facecolor='blue', alpha=0.5)
  
  #print [np.max(elem['err_p']), np.max(sims[name]['y'])]
  mmax = np.max([np.max(elem['err_p']), np.max(sims[name]['y'])])
  ofs = max(round(mmax/2.), 2)
  print mmax, ofs
  
  #plot vertical lines for point location
  for jj, p in enumerate(sorted(elem['pnts'])):
    if   p['t']=='min': c='c'
    elif p['t']=='max': c='r'
    elif p['t']=='sad': c='g'
    plt.plot([p['d'], p['d']], [0,ofs-0.25*jj], c+':')
    plt.text(p['d']+0.1, ofs-0.25*jj, p['t'])

  plt.plot(sims[name]['x'], sims[name]['y'], 'r')
  plt.plot([0,np.max(elem['x'])], [1,1], ':m')  
  
  if cenc:
    plt.suptitle('Analysis for ID: **** - model of: ASW*******', fontsize=14)
    plt.title('by: %s - pixrad: %i - nModels: %i' % (elem['user'], elem['pxR'], elem['nMod']), fontsize=12)
  else:
    plt.suptitle('Analysis for ID: %s - model of: %s' % (elem['id'], name), fontsize=14)
    plt.title('by: %s - pixrad: %i - nModels: %i' % (elem['user'], elem['pxR'], elem['nMod']), fontsize=12)
  #plt.title('Analysis for id: %s, model of: %s by: %s' % (elem['id'], name, elem['user']))
  
  print 'stat:', idd, 
  print 'pixrad :', int(elem['nr'])-1,
  print 'nmodels:', int(elem['nMod'])
  
  
  
  plt.xlabel(r'image radius [pixels]')
  plt.ylabel(r'mean convergance [1]')  
  
  plt.xlim([0,np.max(elem['x'])])
  
  if show:
    print 'show'
    plt.show()
  else:
    #print os.path.join, save_fig_path#, str(idd)+'.png')
    if cenc:
      imgname = ('%03i'%idd) + str(random.randint(1000,9999)) + '.png'
    else:
      imgname = ('%03i'%idd)+'.png'
    plt.savefig(os.path.join(save_fig_path, imgname))
    pass
  
  
def findd(key, val):
  for kk, d in enumerate(data):
    if d[key]==val: print 'index:', kk, 'id:', d['id']
      
      
def plot_all(show=True, cens=False):
  for i in range(len(data)):
    plott(i, show, cens)
    
def plot_all1():
  plot_all(False, True)
  
#plott(56, False, True)
