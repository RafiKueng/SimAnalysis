# -*- coding: utf-8 -*-
"""
collects all the data distributed all over this place and generates the
final plots.

make sure to have the following installed:
- python module 'requests'
- latex modules 'amsmath', 'textgreek'?

should run in this folder /plots, doens't do much by default, you need
to call some command after importing this module that anything happens.
Needs the whole repro to be checked out. (folders /spaghetti and /systems)

either:
  use python in interactive mode:
  python -i -c "import gen_plots"

or (better):
  use ipython:
  ipython
  %run gen_plots.py
  
available commands are:

- run():
  does all the work below
  
- all_sim_plot()
  creates all the simulation data plots ('real' data)
  
- all_mod_plots()
  creates all the results / modells plots
  (server side created plots get grapped from internet)
  
- all_tex()
  assumes the plots are already created (under /plots)
  creates all the tex files and copies the relevant files
  to the tex folder


data is stored in:
- many.sim
- spg.data




Created on Mon Sep 02 15:35:36 2013

@author: RafiK
"""


import sys
import os
import shutil

import requests as rq

import numpy as np
import matplotlib as mpl

mpl.rc('text', usetex=True)
mpl.rc('font', family='serif')

params = {
# see http://matplotlib.org/users/customizing.html
#  'backend': 'ps',
  'text.latex.preamble': [
    r"\usepackage{amsmath}",
    #r"\usepackage{textgreek}"
    ],
  'mathtext.default': 'regular',
  'axes.labelsize': 14,
  'text.fontsize': 14,
  'legend.fontsize': 10,
  'xtick.labelsize': 12,
  'ytick.labelsize': 12,
  'text.usetex': True,
#  'figure.figsize': fig_size,
#  'axes.unicode_minus': True
  }
mpl.rcParams.update(params)

import matplotlib.pylab as pl

from numpy import pi

# set to false to do a dry run in /plots/res
write_to_tex_folder = True
#image extension (png or pdf)
ext = 'png'


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

debug = False



def test():
#  for idd, elem in enumerate(spg.data):
#    mid = elem['id']
#    draw_mod(0, mid, 0, spg.data, spg.sims)
#    break
  for asw in many.sim:
    draw_sim(asw, many.sim)
    break



def run():
  all_sim_plots()
  all_mod_plots()
  all_tex()
  plotAllRE()

#==============================================================================
#   # generate sim plots
#==============================================================================
def all_sim_plots():
  print '\nSIMS'
  print '============================================='  
  for asw in many.sim:

    path = os.path.join(simdir, asw)
    if not os.path.isdir(path):
      os.makedirs(path)    
    
    get_sim_adv_data(asw)
    draw_sim(asw, many.sim)
    if debug: break
  
#==============================================================================
#   # generate models plots
#==============================================================================
def all_mod_plots():
  print '\nMODS'
  print '============================================='  
  for idd, elem in enumerate(spg.data):
    
    mid = elem['id']

    path = os.path.join(moddir, '%06i'%mid)
    if not os.path.isdir(path):
      os.makedirs(path)    

    get_mod_adv_data(mid) #download plots generated on server with glass
    draw_mod(mid, elem, spg.data, spg.sims)

    if debug: break
  
  
  
#==============================================================================
#   # create tex folder / files for easy include
#==============================================================================
def all_tex():
  print '\nTEX'
  print '============================================='
  mid_list = []
  for idd, elem in enumerate(spg.data):

    mid = elem['id']
    asw = elem['name']
    
      
    spath = os.path.join(resdir, asw)
    mpath = os.path.join(resdir, '%06i'%mid)
    for path in [spath, mpath]:
      #print path
      if not os.path.isdir(path):
        os.makedirs(path)

    t1 = copy_model_files(mid)
    t2 = copy_sim_files(asw)
    
    #only create tex file if all files available and copied    
    if t1 and t2:
      create_tex(mid, asw)
      create_alt_tex(mid, asw)
      mid_list.append(str(mid))
    if debug: break
  
  with open(os.path.join(resdir, '_all.tex'), 'w') as ff:
    ff.write('\n'.join(['\input{fig/sims/%s}\n\clearpage'%_ for _ in mid_list]))

  with open(os.path.join(resdir, '_all_alt.tex'), 'w') as ff:
    ff.write('\n'.join(['\input{fig/sims/%s_alt}\n\clearpage'%_ for _ in mid_list]))

class tFig(dict):
  def __init__(self, sf_path, sf_capt, sf_label, sf_opt):
    self.sf_path = sf_path
    self.sf_capt = sf_capt
    self.sf_label = sf_label
    self.sf_opt = sf_opt
    
  def __getitem__(self, key):
    return self.__dict__[key]
    
  
def create_tex(mid, asw):
  
  print '> generating tex file',mid,
  
  sf_opt = r'[width=0.45\textwidth]'
  txFigs = [
    tFig(
      r'fig/sims/%s/kappa.%s'%(asw, ext),
      r'[real mass distribution]',
      r'%04i_sim_mass' % mid,
      sf_opt
    ),
    tFig(
      r'fig/sims/%s/arriv.%s'%(asw, ext),
      r'[real arrival-time surface]',
      r'%04i_sim_arr' % mid,
      sf_opt
    ),  
    tFig(
      r'fig/sims/%06i/mass.%s'%(mid, ext),
      r'[model mass distribution]',
      r'%04i_mass'%mid,
      sf_opt
    ),  
    tFig(
      r'fig/sims/%06i/spaghetti.%s'%(mid, ext),
      r'[model arrival-time surface]',
      r'%04i_cont'%mid,
      sf_opt
    ),  
    tFig(
      r'fig/sims/%06i/kappa_encl.%s'%(mid, ext),
      r'[real vs model enclosed mass]',
      r'%04i_kappa'%mid,
      sf_opt
    ),  
    tFig(
      r'fig/sims/%06i/arr_time.%s'%(mid, ext),
      r'[model lensed image]',
      r'%04i_atime'%mid,
      sf_opt
    ),
  ]

  #figpath = os.path.join(resdir, '%06i'%mid)
  texpath = resdir

#  try:
#    figpath = os.path.join(resdir, '%06i'%mid)
#    texpath = resdir
#    #os.makedirs(figpath)
#  except OSError as e:
#    print 'error creating dir', e

  tex_env = r"""
\begin{figure}
  \centering
%(subfigtex)s
  \caption%(env_capt_short)s{%(env_capt_long)s}
  \label{fig:%(env_label)s}
\end{figure}
  """
  
  tex_sub = r"""  \subfigure%(sf_capt)s{
    \label{fig:%(sf_label)s}
    \includegraphics%(sf_opt)s{%(sf_path)s}
  }
"""

  subfigtex = ''
  
  for fig in txFigs:
    data = {
#      'sf_path'   : r'fig/sims/%06i/img.%s' % (mid, ext),
#      'sf_capt'   : r'[some capt]',
#      'sf_label'  : r'tmplbl',
#      'sf_opt'    : r'[width=0.3\textwidth]'
    }
    subfigtex += tex_sub % fig
    
  data = {
    'subfigtex'      : subfigtex,
    'env_capt_short' : r'[result %4i (%s)]' % (mid, asw),
    'env_capt_long'  : r'data for result %4i, of %s' % (mid, asw),
    'env_label'      : r'%04i'%mid,
  }
  
  tex = tex_env % data
  
  with open(os.path.join(texpath, '%04i.tex'%mid), 'w') as ff:
    ff.write(tex)

  print '...DONE.'
  print '  - %04i.tex'%mid



def create_alt_tex(mid, asw):
  '''creates tex files for alternative arrangement (to compare point placement)
  you have to manually copy the output of many2 into the sims folder..  
  '''
  print '> generating alt tex file',mid,
  
  sf_opt = r'[height=0.4\vsize]'
  
  txFigs = [
    tFig(
      r'fig/sims/%s/arriv.%s'%(asw, ext),
      r'[real arrival-time surface]',
      r'%04i_sim_arr' % mid,
      sf_opt
    ),  
    tFig(
      r'fig/sims/%06i/spaghetti.%s'%(mid, ext),
      r'[model arrival-time surface]',
      r'%04i_cont'%mid,
      sf_opt
    ),  
    tFig(
      r'fig/sims/%s/extr_points.%s'%(asw, ext),
      r'[sw image]',
      r'%04i_sw'%mid,
      sf_opt
    ),  
    tFig(
      r'fig/sims/%06i/input.%s'%(mid, ext),
      r'[input image]',
      r'%04i_input'%mid,
      sf_opt
    ),
  ]

  #figpath = os.path.join(resdir, '%06i'%mid)
  texpath = resdir

#  try:
#    figpath = os.path.join(resdir, '%06i'%mid)
#    texpath = resdir
#    #os.makedirs(figpath)
#  except OSError as e:
#    print 'error creating dir', e

  tex_env = r"""
\begin{figure}
  \centering
%(subfigtex)s
  \caption%(env_capt_short)s{%(env_capt_long)s}
  \label{fig:%(env_label)s}
\end{figure}
  """
  
  tex_sub = r"""  \subfigure%(sf_capt)s{
    \label{fig:%(sf_label)s}
    \includegraphics%(sf_opt)s{%(sf_path)s}
  }
"""

  tex = []
  for i in [0,1]:
    subfigtex = ''
    
    for fig in txFigs[i*2:i*2+2]:
      subfigtex += tex_sub % fig
      
    data = {
      'subfigtex'      : subfigtex,
      'env_capt_short' : r'[result %4i (%s)]' % (mid, asw),
      'env_capt_long'  : r'data for result %4i, of %s' % (mid, asw),
      'env_label'      : r'%04i.%i'%(mid,i),
    }
    
    tex.append(tex_env % data)
  
  with open(os.path.join(texpath, '%04i_alt.tex'%mid), 'w') as ff:
    s = '\n'+r'\clearpage'+'\n'
    ff.write(s.join(tex))

  print '...DONE.'
  print '  - %04i_alt.tex'%mid

import csv
def create_csv():
  '''creates an overview in csv format over results and models'''

  path = os.path.join(outdir,'overview.csv')  
  
  s = {}
  for d in spg.data:
    name = d['name']
    try:
      s[name]
    except KeyError:
      s[name] = []
    s[name].append(d)
    
  with open(path, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for key, val in s.items():
      writer.writerow([key])
      for v in val:
        writer.writerow(['',v['id'],v['nPnt'],v['user']])
      
    

def copy_model_files(mid):
  '''copies files to the final desination, with right ordering'''
  
  print '> copying model files',
  
  figpath = os.path.join(resdir, '%06i'%mid)
  
  imgpath = os.path.join(moddir, '%06i'%mid)

  imgs = os.listdir(imgpath)
  imgs = [_ for _ in imgs if _.endswith('.%s'%ext)]
  #imgs = ['']
  
  for img in imgs:
    ipath = os.path.join(imgpath, img)
    try:
      shutil.copy2(ipath, figpath)
      print '.',
    except OSError:
      print '!! copy error', mid
      return False

  print ' ...DONE.'
  for f in imgs: print '  - %s'%f
  return True

def copy_sim_files(asw):
  '''copies files to the final desination, with right ordering'''

  print '> copying sim files',

  figpath = os.path.join(resdir, asw)
  imgpath = os.path.join(simdir, asw)
  try:  
    files = os.listdir(imgpath)
  except OSError:
    print ' ... FAILED'
    print '!! sim not found:', asw, imgpath
    return False
  for f in files:
    if f.endswith('.%s'%ext):
      try:
        shutil.copy2(os.path.join(imgpath,f), figpath)
      except:
        print '!! file not found:', os.path.join(imgpath,f)
      print '.',

  print ' ...DONE.'
  for f in files: print '  - %s'%f
  return True
    

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
  print '> getting model data online', 
  
  baseurl = 'http://mite.physik.uzh.ch/script_output/gen_plots_for_paper/%06i/' %mid
  
  imgs = ['img1', 'img2', 'img3']
  saveas = ['spaghetti', 'mass', 'arr_time']

  #append eextension
  imgs = [_+'.%s'%ext for _ in imgs]
  saveas = [_+'.%s'%ext for _ in saveas]

  path = os.path.join(moddir, '%06i'%mid)
  

  for k, img in enumerate(imgs):
    r = rq.get(baseurl+img, stream=True)
    if r.status_code == 200:
      with open(os.path.join(path, saveas[k]), 'wb') as f:
        for chunk in r.iter_content(1024):
          f.write(chunk)
    else:
      print '!! file', baseurl, img, 'not found'
  
  # get input image
  r = rq.get('http://mite.physik.uzh.ch/result/%06i/input.png'%mid, stream=True)
  if r.status_code == 200:
    with open(os.path.join(path, 'input.png'), 'wb') as f:
      for chunk in r.iter_content(1024):
        f.write(chunk)
  else:
    print '!! file input.png not found'
  
  print '...DONE.'
  for f in saveas: print '  - %s'%f
  print '  - input.png'


def get_sim_adv_data(asw):
  """gets some online data"""
  print '> getting sims data online', 

  path = os.path.join(simdir, asw)

  #get sw image
  data = {
    'action': 'datasourceApi',
    'src_id':3,
    'do':'fetch',
    'swid': asw
    }
  r=rq.post('http://mite.physik.uzh.ch/api', data)
  if r.status_code == 200:
    iurl = r.json()['list'][0]['url']
    
    r = rq.get(iurl, stream=True)
    if r.status_code == 200:
      with open(os.path.join(path, 'sw.png'), 'wb') as f:
        for chunk in r.iter_content(1024):
          f.write(chunk)
    else:
      print '!! file on spacewarps not found'        
    
  else:
    pass

  print '...DONE.'
  print '  - sw.png'


def draw_sim(asw, sim):
  
    path = os.path.join(simdir, asw)
#    try:
#      path = os.path.join(simdir, asw)
#      #os.makedirs(path)
#    except OSError as e:
#      print 'error creating dir', e
#      #return

    filenames = ['arriv', 'kappa', 'm_encl']
    
    print '> drawing sim %s'%asw,    
    
    #prevent submodules prints..
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    devnull = open(os.devnull, 'w')
    sys.stdout = devnull
    #sys.stderr = devnull
      
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
    pl.savefig(os.path.join(path, '%s.%s'%(filenames[1],ext)))


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
    fil = open(os.path.join(simdir, asw+'.txt'),'w')
    for k in range(len(rad)):
        fil.write('%9.2e %9.2e\n' % (rad[k],sum[k]))
    fil.close()
    panel.scatter(rad,sum)
    panel.set_xlabel('radius [pixels]')
    panel.set_ylabel('average interior \textkappa [1]')
    pl.savefig(os.path.join(path, '%s.%s'%(filenames[2],ext)))
    
    
    fig = pl.figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lo,hi = np.amin(arriv), np.amax(arriv)
    lev = np.linspace(lo,lo+.2*(hi-lo),100)
    panel.contour(x,y,arriv,lev)
    pl.savefig(os.path.join(path, '%s.%s'%(filenames[0],ext)))

    #restore stdout
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
    print '...DONE.'
    for f in filenames: print '  - %s'%(f+'.'+ext)


def draw_mod(mid, elem, data, sims):
#def plot2(idd, count):

  plot_rE = True
  print_rE = True
  prnt = False
  show = False
  save_fig_path = os.path.join(moddir, '%06i'%mid)

#  try:
#    os.mkdir(save_fig_path)
#  except OSError as e:
#    print 'could not create folder', e
    #return
    
  name = elem['name']
  user = elem['user']
  
  if prnt:
    print '...drawing modelling result', mid, name, user
  else:
    print '> drawing modres %06i'%mid,
  
  # create info files
  with open(os.path.join(save_fig_path, name + '.txt'), 'a'):
    pass
  with open(os.path.join(save_fig_path, user + '.txt'), 'a'):
    pass
  

  try:
    sims[name]
  except KeyError:
    print '\n!! missing sims data for', mid, name
    return

  #yerr=[elem['err_p'] - elem['y'], elem['y']- elem['err_m']]


  if plot_rE or print_rE:
    rE_mean = spg.getEinsteinR(elem['x'], elem['y'])
    #rE_max = spg.getEinsteinR(elem['x'], elem['err_p'])
    #rE_min = spg.getEinsteinR(elem['x'], elem['err_m'])
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
  t_props = {'ha':'left', 'va':'bottom', 'fontsize':params['text.fontsize']} 
    
    
  pl.ioff()
  pl.figure()
  #panel = fig.add_subplot(1,1,1)
  
  x  = elem['x']
  #y  = elem['y']
  yp = elem['err_p']
  ym = elem['err_m']
  
  # get interpolated values
  x_ip  = np.linspace(np.min(x), np.max(x), 1000)
  #y_ip  = np.interp(x_ip, x, y)
  yp_ip = np.interp(x_ip, x, yp)
  ym_ip = np.interp(x_ip, x, ym)
  
  #genrate mask, only values between the extr. points
  pnts_x = [_['d'] for _ in elem['pnts'] ]
  mask = (x_ip > np.min(pnts_x)) & (x_ip < np.max(pnts_x))
  

  #plot the model values
  pl.plot(elem['x'], elem['err_p'], 'b')
  pl.plot(elem['x'], elem['err_m'], 'b')
  pl.fill_between(x_ip[mask], yp_ip[mask], ym_ip[mask], facecolor='blue', alpha=0.5)

  
  #plot vertical lines for point location
  for jj, p in enumerate(sorted(elem['pnts'])):
    if   p['t']=='min': c='c'
    elif p['t']=='max': c='r'
    elif p['t']=='sad': c='g'
    pl.plot([p['d'], p['d']], [0,ofs-t_dt*jj], c+':')
    pl.text(p['d']+t_dx, ofs-t_dt*jj+t_dy, p['t'], **t_props)

  # plot simulation parameter data
  pl.plot(sims[name]['x'], sims[name]['y'], 'r')
  pl.plot([0,np.max(elem['x'])], [1,1], ':m')  
  
  #titles etc
  #pl.suptitle('Analysis for ID: %s - model of: %s' % (elem['id'], name), fontsize=18)
  #pl.title('by: %s - pixrad: %i - nModels: %i' % (r'\verb|%s|'%elem['user'], elem['pxR'], elem['nMod']), fontsize=14)
  

#  if prnt:
#    print 'stat:', idd, 
#    print 'pixrad :', int(elem['nr'])-1,
#    print 'nmodels:', int(elem['nMod']),
#  if prnt & print_rE:
#    print 'rE_models = %4.2f [%4.2f...%4.2f] rE_sim = %4.2f' % (rE_mean, rE_min, rE_max, rE_data)
#  elif prnt:
#    print ''
    
  # plot einsteinradius
  if plot_rE:
    #a_re_min = np.array([rE_min, rE_min])
    #a_re_max = np.array([rE_max, rE_max])
    a_re_mean = np.array([rE_mean, rE_mean])
    a_re_data = np.array([rE_data, rE_data])
    #fbx2 = rE_max
    #fby = np.array([0.5,rE_pos-0.25])
    #fby = np.array([0.5,1,1.5])
    #a2_re_min = np.array([rE_min, rE_min, rE_min])
    #a2_re_max = np.array([rE_max, rE_max, rE_max])

    pl.plot(a_re_mean, [0,rE_pos], '--', color=(0,0.5,0))
    pl.text(rE_mean+t_dx, rE_pos+t_dy, r'$\Theta _\text{E}$ = %4.2f'%(rE_mean), **t_props)
    #pl.plot(a_re_min, [0,rE_pos-0.25], ':b')
    #pl.plot(a_re_max, [0,rE_pos-0.25], ':b')

    #if prnt: print a_re_min, fbx2, fby
    
    #pl.fill_betweenx(fby,a2_re_min, a2_re_max, alpha=0.3, edgecolor='white', facecolor=['cyan','green'], cmap=pl.cm.Accent) #facecolor='cyan',
    
    #cp1 = 0.0
    #cp2 = 1.0
    #cy = np.ones(rE_pos*4) # spaced in 1/4 steps, rE_pos is int!
    #cy[0]=0
    #cy[1]=0.5
    #cy[-1]=0
    #cy[-2]=0.5
    
    #cy = np.array([cy,cy]).transpose()
    
    pl.plot(a_re_data, [0,rE_pos+t_dt], '--r')
    pl.text(rE_data+t_dx, rE_pos+t_dt+t_dy, r'$\Theta_\text{E,sim}$ = %4.2f'%(rE_data), **t_props)
    

  
  
  pl.xlabel(r'image radius [pixels]')
  pl.ylabel(r'mean convergance [1]')  
  
  pl.xlim([0,np.max(elem['x'])])
  
  if show:
    #print 'show'
    pl.show()
  else:
    imgname = ('kappa_encl.%s'%ext)
    pl.savefig(os.path.join(save_fig_path, imgname))
    pass
  
  
  print ' ... DONE.'
  print '  - %s' % imgname

tmp={}
def plotAllRE():
  '''plots the final big scatter plot with all rE'''
  print '> drawing EinsteinR plots',

  plots = [True, True, True, True]
  #plots = [0, 0, 0, True]
  
  path = resdir

  spg.genREData() # genreate the data

  #collect data
  sims = {}
  lu = {}
  for i, item in enumerate(spg.sims.items()):
    key, val = item
    sims[key] = val['rE']
    lu[key] = i
    
  xi = []
  re = []
  ep = []
  em = []
  re_rel = []
  ep_rel = []
  em_rel = []
  se = []
  for dat in spg.data:
    try:
      re_sim = sims[dat['name']]
    except KeyError:
      continue
    se.append(re_sim)
    xi.append(dat['id'])
    re.append(dat['rE_mean'])
    ep.append(dat['rE_max'])
    em.append(dat['rE_min'])
    re_rel.append(dat['rE_mean']/re_sim)
    ep_rel.append(dat['rE_max']/re_sim)
    em_rel.append(dat['rE_min']/re_sim)
    
  xi = np.array(xi)
  re = np.array(re)
  ep = np.array(ep) - re
  em = re - np.array(em)
  ee = [ep, em]
  re_rel = np.array(re_rel)
  ep_rel = np.array(ep_rel) - re_rel
  em_rel = re_rel - np.array(em_rel)
  ee_rel = [ep_rel, em_rel]
  
  if plots[0]:
    pl.figure()
    pl.errorbar(xi, re, ee, marker='s', mfc='blue', ls='' ,ecolor='blue')
    pl.plot(xi, se, 'rx')
    
    pl.savefig(os.path.join(path, 'eR_1.png'))
    print '.',
    #pl.show()
  
  if plots[1]:  
    pl.figure()
    pl.errorbar(xi, re_rel, ee_rel, marker='s', mfc='blue', ls='' ,ecolor='blue')
    pl.plot(xi, xi*0+1, '-r')
    
    pl.savefig(os.path.join(path, 'eR_2.png'))
    print '.',
    #pl.show()
  
  if plots[2]:
    pl.figure()
    for i, dat in enumerate(spg.data):
      simn = dat['name']    
      try:
        lu[simn]
      except KeyError:
        continue
      pl.plot(lu[simn], dat['rE_mean'], 'bx')
      
    lbls = [key for key, val in spg.sims.items()]
    for i, item in enumerate(spg.sims.items()):
      key, val = item
      try:
        pl.plot(lu[key], val['rE'], 'rs')
      except KeyError:
        continue
      #lbls[i] = key
      
    pl.xticks(range(i+1), lbls, rotation=90)
    pl.gcf().subplots_adjust(bottom=0.2)
    pl.xlim([-.5, i+0.5])
    pl.ylabel(r'Einstein Radius $\Theta_{\text{E}}$')

    pl.savefig(os.path.join(path, 'eR_3.png'))
    print '.',
    #pl.show()
    
  if plots[3]:
    pl.figure()
    for i, dat in enumerate(spg.data):
      simn = dat['name']    
      try:
        lu[simn]
      except KeyError:
        continue
      style = 'rx' if dat['user']=='psaha' else 'bx'
      xofs = 0.15 if dat['user']=='psaha' else -0.15
      pl.plot(lu[simn]+xofs, dat['rE_mean']/sims[simn], style)
      
    lbls = [key for key, val in spg.sims.items()]
    for i, item in enumerate(spg.sims.items()):
      key, val = item
    pl.plot([-0.5, i+0.5], [1,1], '--r')
    
    pl.xticks(range(i+1), lbls, rotation=90)
    pl.yticks(np.linspace(0,2,(2/0.25)+1))
    pl.grid(axis='y')
    pl.gcf().subplots_adjust(bottom=0.2)
    pl.xlim([-.5, i+0.5])
    pl.ylabel(r'rel Einstein Radius $\Theta_{\text{E}}$/$\Theta_{\text{E, sim}}$')

    pl.savefig(os.path.join(path, 'eR_4.png'))
    print '.',
    #pl.show()
    
  print ' ... DONE'
