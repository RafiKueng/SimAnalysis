# -*- coding: utf-8 -*-
"""
collects all the data distributed all over this place and generates the
final plots

Created on Mon Sep 02 15:35:36 2013

@author: RafiK
"""


import sys
import os
import shutil

import requests as rq

import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl

from numpy import pi

write_to_tex_folder = False

# realtive to plots dir
outdir = 'figs'

simdir = 'sim'
moddir = 'mod'



resdir = 'res'
# relative to root of git repro
texdir = 'text/fig/sims'



pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), outdir))
simdir = os.path.abspath(os.path.join(outdir, simdir))
moddir = os.path.abspath(os.path.join(outdir, moddir))

if write_to_tex_folder:
  resdir = os.path.abspath(os.path.join(pardir, texdir))
else:
  resdir = os.path.abspath(os.path.join(outdir, resdir))


sys.path.append(os.path.join(pardir, 'spaghetti'))
sys.path.append(os.path.join(pardir, 'systems'))

import gen_kappa_encl_plots as spg
import many


def tmp():
  for asw in many.sim:
    draw_sim(asw, many.sim)
    break
  
  for idd, elem in enumerate(spg.data):
    draw_mod(0, elem['id'], 0, spg.data, spg.sims)
    break
  
  for idd, elem in enumerate(spg.data):
    create_tex(elem['id'], None)
    break
    
  
  
def create_tex(mid, asw):
  try:
    figpath = os.path.join(resdir, '%06i'%mid)
    texpath = resdir
    os.makedirs(figpath)
  except OSError as e:
    print 'error creating dir', e

  rawtex = r"""
\begin{figure}
  \centering
    \includegraphics[width=0.45\textwidth]{%s}
  \caption{%s}
  \label{fig:%s}
\end{figure}
"""

  tex = ''
  
  for i in range(1):
    figpath_rel = 'fig/sims/%06i/'
    capt =  'tmpdesc'
    lbl = 'tmplbl'
    tex += rawtex % (figpath_rel, capt, lbl)
    
  
  
  with open(os.path.join(texpath, '%06i.tex'%mid), 'w') as ff:
    ff.write(tex)
    
  #copy files
  img = os.path.join(moddir, os.path.join('%06i'%mid, '006904_ASW0003ctp_Jonas.png'))
  shutil.copy2(img, figpath)
  
    

def get_mod_def_data(mid):
  """gets the deault data directly from mite web"""
  baseurl = 'http://mite.physik.uzh.ch/result/%06i/' %mid
  
  imgs = ['img2.png', 'img3.png']
  saveas = ['mass.png', 'arr_time.png']

  path = os.path.join(moddir, '%06i'%mid)

  for k, img in enumerate(imgs):
    r = rq.get(baseurl+img, stream=True)
    if r.status_code == 200:
      with open(os.path.join(path, saveas[k]), 'wb') as f:
        for chunk in r.iter_content(1024):
          f.write(chunk)
          


def get_mod_adv_data(mid):
  """gets the better plots produced by script"""
  baseurl = 'http://mite.physik.uzh.ch/script_output/gen_plots_for_paper/%06i/' %mid
  
  imgs = ['img2.png', 'img3.png']
  saveas = ['mass.png', 'arr_time.png']

  path = os.path.join(moddir, '%06i'%mid)

  for k, img in enumerate(imgs):
    r = rq.get(baseurl+img, stream=True)
    if r.status_code == 200:
      with open(os.path.join(path, saveas[k]), 'wb') as f:
        for chunk in r.iter_content(1024):
          f.write(chunk)
          



def draw_sim(asw, sim):
    try:
      path = os.path.join(simdir, asw)
      os.mkdir(path)
    except OSError as e:
      print 'error creating dir', e
      #return
      
      
    print asw
    N,R = 100,50
    if sim[asw][0] == 'quasar':
        flag,R = 'Q',20
    if sim[asw][0] == 'galaxy':
        flag,R = 'G',20
    if sim[asw][0] == 'cluster':
        flag,R = 'C',50
    x = np.linspace(-R,R,N)
    y = 1*x
    kappa,arriv = many.grids(asw,x,y)
    fig = pl.figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lev = np.linspace(0,10,41)
    pc = panel.contour(x,y,kappa,lev)
    panel.clabel(pc, inline=1, fontsize=10)
    pl.savefig(os.path.join(path, asw+flag+'_kappa.png'))
    fig = pl.figure()
    panel = fig.add_subplot(1,1,1)
    rad = np.linspace(0,R,20)[1:]
    radq = rad*rad
    sum = 0*rad
    for i in range(len(x)):
        for j in range(len(y)):
            rsq = x[i]**2 + y[j]**2
            for k in range(len(rad)):
                if rsq < radq[k]:
                    sum[k] += kappa[j,i]
    dx = x[1]-x[0]
    for k in range(len(rad)):
        sum[k] *= dx*dx/(pi*radq[k])
    fil = open(os.path.join(path, asw+'.txt'),'w')
    for k in range(len(rad)):
        fil.write('%9.2e %9.2e\n' % (rad[k],sum[k]))
    fil.close()
    panel.scatter(rad,sum)
    panel.set_xlabel('radius in pixels')
    panel.set_ylabel('average interior $\kappa$')
    pl.savefig(os.path.join(path, asw+flag+'_menc.png'))
    fig = pl.figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lo,hi = np.amin(arriv), np.amax(arriv)
    lev = np.linspace(lo,lo+.2*(hi-lo),100)
    panel.contour(x,y,arriv,lev)
    pl.savefig(os.path.join(path, asw+flag+'_arriv.png'))






def draw_mod(idd, mid, count, data, sims):
#def plot2(idd, count):

  plot_rE = True
  print_rE = True
  show = False
  cens = False
  save_fig_path = os.path.join(moddir, '%06i'%mid)
  try:
    os.mkdir(save_fig_path)
  except OSError as e:
    print 'could not create folder', e
    #return
    

  elem = data[idd]
  name = elem['name']

  try:
    sims[name]
  except KeyError:
    print '!! missing sims data for', idd, name
    return

  yerr=[elem['err_p'] - elem['y'], elem['y']- elem['err_m']]


  if plot_rE or print_rE:
    rE_mean = spg.getEinsteinR(elem['x'], elem['y'])
    rE_max = spg.getEinsteinR(elem['x'], elem['err_p'])
    rE_min = spg.getEinsteinR(elem['x'], elem['err_m'])
    rE_data = spg.getEinsteinR(sims[name]['x'], sims[name]['y'])

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
    
    
  pl.ioff()
  fig = pl.figure()
  #panel = fig.add_subplot(1,1,1)
  

  #pl.errorbar(elem['x'], elem['y'], yerr=yerr)
  pl.plot(elem['x'], elem['err_p'], 'b')
  pl.plot(elem['x'], elem['err_m'], 'b')
  #pl.plot(elem['x'], elem['y'], 'k')
  pl.fill_between(elem['x'], elem['err_p'], elem['err_m'], facecolor='blue', alpha=0.5)
  
  #print [np.max(elem['err_p']), np.max(sims[name]['y'])]
  #print mmax, ofs
  
  #plot vertical lines for point location
  for jj, p in enumerate(sorted(elem['pnts'])):
    if   p['t']=='min': c='c'
    elif p['t']=='max': c='r'
    elif p['t']=='sad': c='g'
    pl.plot([p['d'], p['d']], [0,ofs-t_dt*jj], c+':')
    pl.text(p['d']+t_dx, ofs-t_dt*jj+t_dy, p['t'], **t_props)

  pl.plot(sims[name]['x'], sims[name]['y'], 'r')
  pl.plot([0,np.max(elem['x'])], [1,1], ':m')  
  
  if cens:
    pl.suptitle('Analysis for ID: **** - model of: ASW*******', fontsize=14)
    pl.title('by: %s - pixrad: %i - nModels: %i' % (elem['user'], elem['pxR'], elem['nMod']), fontsize=12)
  else:
    pl.suptitle('Analysis for ID: %s - model of: %s' % (elem['id'], name), fontsize=14)
    pl.title('by: %s - pixrad: %i - nModels: %i' % (elem['user'], elem['pxR'], elem['nMod']), fontsize=12)
  #pl.title('Analysis for id: %s, model of: %s by: %s' % (elem['id'], name, elem['user']))
  
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

    pl.plot(a_re_mean, [0,rE_pos], '--', color=(0,0.5,0))
    pl.text(rE_mean+t_dx, rE_pos+t_dy, '$r_E$ = %4.2f [%4.2f .. %4.2f]'%(rE_mean, rE_min, rE_max), **t_props)
    #pl.plot(a_re_min, [0,rE_pos-0.25], ':b')
    #pl.plot(a_re_max, [0,rE_pos-0.25], ':b')

    print a_re_min, fbx2, fby
    
    #pl.fill_betweenx(fby,a2_re_min, a2_re_max, alpha=0.3, edgecolor='white', facecolor=['cyan','green'], cmap=pl.cm.Accent) #facecolor='cyan',
    
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
    
    pl.imshow(cy, interpolation='bilinear', cmap=cmblue, extent=(rE_min, rE_max, 0.0, rE_pos), alpha=0.7, aspect='auto')
  
    pl.plot(a_re_data, [0,rE_pos+t_dt], '--r')
    pl.text(rE_data+t_dx, rE_pos+t_dt+t_dy, '$r_E$,sim = %4.2f'%(rE_data), **t_props)
    

  
  
  pl.xlabel(r'image radius [pixels]')
  pl.ylabel(r'mean convergance [1]')  
  
  pl.xlim([0,np.max(elem['x'])])
  
  if show:
    #print 'show'
    pl.show()
  else:
    #print os.path.join, save_fig_path#, str(idd)+'.png')
    if cens:
      imgname = ('%03i'%idd) + str(random.randint(1000,9999)) + '.png'
    else:
      #imgname = ('%03i'%idd)+'.png'
      imgname = ('%06i_%s_%s'%(elem['id'], elem['name'], elem['user']))+'.png'
    pl.savefig(os.path.join(save_fig_path, imgname))
    print os.path.join(save_fig_path, imgname)
    pass
