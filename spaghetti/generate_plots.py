# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:18:42 2013

@author: rafik
"""

import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

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
def plott(idd, show=True, cens=False, plot_rE=False, print_rE=False):

  elem = data[idd]
  name = elem['name']

  try:
    sims[name]
  except KeyError:
    print '!! missing sims data for', idd, name
    return

  yerr=[elem['err_p'] - elem['y'], elem['y']- elem['err_m']]


  if plot_rE or print_rE:
    rE_mean = getEinsteinR(elem['x'], elem['y'])
    rE_max = getEinsteinR(elem['x'], elem['err_p'])
    rE_min = getEinsteinR(elem['x'], elem['err_m'])
    rE_data = getEinsteinR(sims[name]['x'], sims[name]['y'])

  # plotting settings
  ############################

  #where (y val) to start plotting the extr points markers
  mmax = np.max([np.max(elem['err_p']), np.max(sims[name]['y'])])
  ofs = max(round(mmax*0.5), 2) 
  rE_pos = max(round(mmax*0.75), 3) # there to draw the einsteinradius text
  # text offsets and properties
  t_dx = 0.0
  t_dy = 0.1
  t_dt = mmax/16.
  t_props = {'ha':'left', 'va':'bottom'} 
    
    
  plt.ioff()
  fig = plt.figure()
  #panel = fig.add_subplot(1,1,1)
  

  #plt.errorbar(elem['x'], elem['y'], yerr=yerr)
  plt.plot(elem['x'], elem['err_p'], 'b')
  plt.plot(elem['x'], elem['err_m'], 'b')
  #plt.plot(elem['x'], elem['y'], 'k')
  plt.fill_between(elem['x'], elem['err_p'], elem['err_m'], facecolor='blue', alpha=0.5)
  
  #print [np.max(elem['err_p']), np.max(sims[name]['y'])]
  #print mmax, ofs
  
  #plot vertical lines for point location
  for jj, p in enumerate(sorted(elem['pnts'])):
    if   p['t']=='min': c='c'
    elif p['t']=='max': c='r'
    elif p['t']=='sad': c='g'
    plt.plot([p['d'], p['d']], [0,ofs-t_dt*jj], c+':')
    plt.text(p['d']+t_dx, ofs-t_dt*jj+t_dy, p['t'], **t_props)

  plt.plot(sims[name]['x'], sims[name]['y'], 'r')
  plt.plot([0,np.max(elem['x'])], [1,1], ':m')  
  
  if cens:
    plt.suptitle('Analysis for ID: **** - model of: ASW*******', fontsize=14)
    plt.title('by: %s - pixrad: %i - nModels: %i' % (elem['user'], elem['pxR'], elem['nMod']), fontsize=12)
  else:
    plt.suptitle('Analysis for ID: %s - model of: %s' % (elem['id'], name), fontsize=14)
    plt.title('by: %s - pixrad: %i - nModels: %i' % (elem['user'], elem['pxR'], elem['nMod']), fontsize=12)
  #plt.title('Analysis for id: %s, model of: %s by: %s' % (elem['id'], name, elem['user']))
  
  print 'stat:', idd, 
  print 'pixrad :', int(elem['nr'])-1,
  print 'nmodels:', int(elem['nMod']),

  if print_rE:
    print 'rE_models = %4.2f [%4.2f...%4.2f] rE_sim = %4.2f' % (rE_mean, rE_min, rE_max, rE_data)
  else:
    print ''
    
  if plot_rE:
    a_re_min = np.array([rE_min, rE_min])
    a_re_max = np.array([rE_max, rE_max])
    a_re_mean = np.array([rE_mean, rE_mean])
    a_re_data = np.array([rE_data, rE_data])
    fbx2 = rE_max
    #fby = np.array([0.5,rE_pos-0.25])
    fby = np.array([0.5,1,1.5])
    a2_re_min = np.array([rE_min, rE_min, rE_min])
    a2_re_max = np.array([rE_max, rE_max, rE_max])

    plt.plot(a_re_mean, [0,rE_pos], '--', color=(0,0.5,0))
    plt.text(rE_mean+t_dx, rE_pos+t_dy, 'r_E = %4.2f [%4.2f .. %4.2f]'%(rE_mean, rE_min, rE_max), **t_props)
    #plt.plot(a_re_min, [0,rE_pos-0.25], ':b')
    #plt.plot(a_re_max, [0,rE_pos-0.25], ':b')

    print a_re_min, fbx2, fby
    
    #plt.fill_betweenx(fby,a2_re_min, a2_re_max, alpha=0.3, edgecolor='white', facecolor=['cyan','green'], cmap=plt.cm.Accent) #facecolor='cyan',
    
    cp1 = 0.0
    cp2 = 1.0
    cy = np.ones(rE_pos*4) # spaced in 1/4 steps, rE_pos is int!
    cy[0]=0
    cy[1]=0.5
    cy[-1]=0
    cy[-2]=0.5
    
    cy = np.array([cy,cy]).transpose()
    #print cy

    #cpatch = [[cp1],[cp2],[cp1]]

    cdict = { 'red':   ((0,1,1),(1,0,0)),
              'green': ((0,1,1),(1,0.5,0.5)),
              'blue':  ((0,1,1),(1,0,0)),
              'alpha': ((0,0,0),(1,1,1))}
              
    cmblue = mpl.colors.LinearSegmentedColormap('TransparentBlue', cdict)
    
    plt.imshow(cy, interpolation='bilinear', cmap=cmblue, extent=(rE_min, rE_max, 0.0, rE_pos), alpha=0.7, aspect='auto')
  
    plt.plot(a_re_data, [0,rE_pos+t_dt], '--r')
    plt.text(rE_data+t_dx, rE_pos+t_dt+t_dy, 'r_E,sim = %4.2f'%(rE_data), **t_props)
    

  
  
  plt.xlabel(r'image radius [pixels]')
  plt.ylabel(r'mean convergance [1]')  
  
  plt.xlim([0,np.max(elem['x'])])
  
  if show:
    #print 'show'
    plt.show()
  else:
    #print os.path.join, save_fig_path#, str(idd)+'.png')
    if cens:
      imgname = ('%03i'%idd) + str(random.randint(1000,9999)) + '.png'
    else:
      imgname = ('%03i'%idd)+'.png'
    plt.savefig(os.path.join(save_fig_path, imgname))
    pass
  
  
def findd(key, val):
  for kk, d in enumerate(data):
    if d[key]==val: print 'index:', kk, 'id:', d['id']
      
      
def plot_all(show=True, cens=False, plot_rE=False, print_rE=False):
  for i in range(len(data)):
    plott(i, show, cens, plot_rE, print_rE)
    
def plot_all1():
  plot_all(0,0,1,1)

# plot_all(False)

#plott(56, False, True)


import scipy.interpolate as interp
import scipy.optimize as optimize

def getERs(idd):
  elem = data[idd]
  rE_mean = getEinsteinR(elem['x'], elem['y'])
  rE_max = getEinsteinR(elem['x'], elem['err_p'])
  rE_min = getEinsteinR(elem['x'], elem['err_m'])
  rE_data = getEinsteinR(sims[name]['x'], sims[name]['y'])
  print 'rE_models = %4.2f [%4.2f...%4.2f] rE_sim = %4.2f' % (rE_mean, rE_min, rE_max, rE_data)


def getEinsteinR(x, y):
    poly = interp.PiecewisePolynomial(x,y[:,np.newaxis])
    
    def one(x):
        return poly(x)-1
    
    x_min = np.min(x)
    x_max = np.max(x)
    x_mid = poly(x[len(x)/2])
    
    rE,infodict,ier,mesg = optimize.fsolve(one, x_mid, full_output=True)
    
    #print rE,infodict,ier,mesg
    
    if (ier==1 or ier==5) and x_min<rE<x_max and len(rE)==1:
      return rE[0]
    elif len(rE)>1:
      for r in rE:
        if x_min<r<x_max:
          return r
    else:
      return False
    





