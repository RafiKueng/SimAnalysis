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
  (server side created plots get grabbed from internet)
  
- all_tex()
  assumes the plots are already created (under /plots)
  creates all the tex files and copies the relevant files
  to the tex folder

by just calling the script from command line:
  python gen_plots
the run() function gets called automatically



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
import csv

import numpy as np
from numpy import pi
import matplotlib as mpl

import PIL

import defaults


defaults.set_mpl()
args = defaults.args



debug = False

# set to false to do a dry run in /plots/[outdir]
write_to_tex_folder = False

#timeintensive dl of online data. only neeeds to be done once
fetch_onlinedata = True

# do which plots of sims?
simplots = {'arriv': True, 'kappa':True, 'kappaenc':False}

#image extension (png or pdf)
#exts = ['png', 'pdf']
exts = ['png']

figsize   = (10,10) 
figsizeER = (10,8)
figsizeKE = (10,8)

# realtive to plots dir, incase of debug
outdir = 'figs_new4'

#select sims to produce plots for (using sel_sim_plots())
sel_sim = [
    'ASW000102p',
    'ASW000195x',
    'ASW0000vqg',
    'ASW0004oux',
    'ASW0001hpf',
    'ASW0000h2m',
    'ASW0002z6f',
]

#select models to produce pots for (using sel_mod_plots())
sel_mod = [
    6915,
    6919,
    6937,
    6941,
    6975,
    6990,
    7020,
    7021,
    7022,
    7024,
    7025,
]

#enable ER plots to produce
ERplots = [True, True, True, True, True]
if debug: ERplots = [0, True, 0, 0, True]



#params = {
## see http://matplotlib.org/users/customizing.html
##  'backend': 'ps',
#  'text.latex.preamble': [
#    r"\usepackage{amsmath}",
#    #r"\usepackage{textgreek}"
#    ],
#  'mathtext.default': 'regular',
#  'axes.labelsize': 14,
#  'text.fontsize': 14,
#  'legend.fontsize': 10,
#  'xtick.labelsize': 12,
#  'ytick.labelsize': 12,
#  'text.usetex': True,
##  'figure.figsize': fig_size,
##  'axes.unicode_minus': True
#  }
#mpl.rcParams.update(params)
#
#mpl.rc('text', usetex=True)
#mpl.rc('font', family='serif')

#############################################################
# END SETTINGS
#############################################################

pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(os.path.join(pardir, 'spaghetti'))
sys.path.append(os.path.join(pardir, 'systems'))

import matplotlib.pylab as pl
import gen_kappa_encl_plots as spg
import many
# import after, to be sure mpl.rc changes are valid


# subdirs, this should be fixed..
simdir = 'sim'
moddir = 'mod'
resdir = 'res'
texdir = 'text/fig/_new' # relative to root of git repro, using _new prefix, so i still have to copy paste the files



outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), outdir))
simdir = os.path.abspath(os.path.join(outdir, simdir))
moddir = os.path.abspath(os.path.join(outdir, moddir))
resdir = os.path.abspath(os.path.join(outdir, resdir))


if write_to_tex_folder:
  resdir = os.path.abspath(os.path.join(pardir, texdir))
  simdir = resdir
  moddir = resdir
  outdir = resdir
  

  

#manual scaling factors

do_scale = True #should i do the scaling?

distance_factor = 0.428           # 
div_scale_factors = 440./500*100  # 
spacewarps_pixsize = 0.185

scales = {}
scales['ASW000102p'] = {}
scales['ASW000102p'][6941] = {
#    Map radius           = 0.1851 [arcsec] Distance to center of outer pixel.
#    Map Extent           = 0.1929 [arcsec] Distance to outer edge of outer pixel.
#    top_level_cell_size  = 0.0154 [arcsec]
#    Map radius           = 1.1168 [kpc]    H0inv=13.7
#    Map Extent           = 1.1633 [kpc]    H0inv=13.7
    'map_r'           : {'arcsec':0.1851, 'kpc': 1.1168},
    'map_e'           : {'arcsec':0.1929, 'kpc': 1.1633},
}
  
scales['ASW000195x'] = {}
scales['ASW000195x'][6975] = {
    # Pixel radius         = 12
    # Map radius           = 0.4118 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.4290 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0343 [arcsec]
    # Map radius           = 2.1836 [kpc]    H0inv=13.7
    # Map Extent           = 2.2746 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1820 [kpc]    H0inv=13.7
    'map_r'           : {'arcsec':0.4118, 'kpc': 2.1836},
    'map_e'           : {'arcsec':0.4290, 'kpc': 2.2746},
}


scales['ASW0001hpf'] = {}
scales['ASW0001hpf'][6915] = {
    # Map radius           = 0.1213 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1264 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0101 [arcsec]
    # Map radius           = 0.7318 [kpc]    H0inv=13.7
    # Map Extent           = 0.7623 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.1213, 'kpc': 0.7318},
    'map_e'           : {'arcsec':0.1264, 'kpc': 0.7623},
}

scales['ASW0002z6f'] = {}
scales['ASW0002z6f'][6919] = {
    # Map radius           = 0.3153 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.3284 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0263 [arcsec]
    # Map radius           = 1.9018 [kpc]    H0inv=13.7
    # Map Extent           = 1.9810 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.3153, 'kpc':1.9018 },
    'map_e'           : {'arcsec':0.3284, 'kpc':1.9810 },
}

scales['ASW0000vqg'] = {}
scales['ASW0000vqg'][6937] = {
    # Map radius           = 0.2163 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2253 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0180 [arcsec]
    # Map radius           = 0.7024 [kpc]    H0inv=13.7
    # Map Extent           = 0.7316 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.2163, 'kpc':0.7024 },
    'map_e'           : {'arcsec':0.2253, 'kpc':0.7316 },
}

scales['ASW000102p'] = {}
scales['ASW000102p'][6941] = {
    # Map radius           = 0.1851 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1929 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0154 [arcsec]
    # Map radius           = 1.1168 [kpc]    H0inv=13.7
    # Map Extent           = 1.1633 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.1851, 'kpc':1.1168 },
    'map_e'           : {'arcsec':0.1929, 'kpc':1.1633 },
}

scales['ASW000195x'] = {}
scales['ASW000195x'][6975] = {
    # Pixel radius         = 12
    # Map radius           = 0.4118 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.4290 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0343 [arcsec]
    # Map radius           = 2.1836 [kpc]    H0inv=13.7
    # Map Extent           = 2.2746 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1820 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0

    'map_r'           : {'arcsec':0.4118, 'kpc':2.1836 },
    'map_e'           : {'arcsec':0.4290, 'kpc':2.2746 },
}

scales['ASW0004oux'] = {}
scales['ASW0004oux'][6990] = {
    # Pixel radius         = 12
    # Map radius           = 0.2618 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2727 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0218 [arcsec]
    # Map radius           = 1.5794 [kpc]    H0inv=13.7
    # Map Extent           = 1.6452 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1316 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0

    'map_r'           : {'arcsec':0.2618, 'kpc':1.5794 },
    'map_e'           : {'arcsec':0.2727, 'kpc':1.6452 },
}


scales['ASW0000h2m'] = {}
'''
scales['ASW0000h2m'][7020] = {
    # Pixel radius         = 12
    # Map radius           = 0.1868 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1946 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0156 [arcsec]
    # Map radius           = 1.1266 [kpc]    H0inv=13.7
    # Map Extent           = 1.1735 [kpc]    H0inv=13.7
    # top_level_cell       = 0.0939 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0
    
    'map_r'           : {'arcsec':0.1868, 'kpc':1.1266 },
    'map_e'           : {'arcsec':0.1946, 'kpc':1.1735 },
}
'''
'''
scales['ASW0000h2m'][7021] = {
    # Pixel radius         = 12
    # Map radius           = 0.1993 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2076 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0166 [arcsec]
    # Map radius           = 1.2022 [kpc]    H0inv=13.7
    # Map Extent           = 1.2523 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1002 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    'map_r'           : {'arcsec':0.1993, 'kpc':1.2022 },
    'map_e'           : {'arcsec':0.2076, 'kpc':1.2523 },
}
'''
scales['ASW0000h2m'][7022] = {
    # Pixel radius         = 12
    # Map radius           = 0.1895 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1973 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0158 [arcsec]
    # Map radius           = 1.1427 [kpc]    H0inv=13.7
    # Map Extent           = 1.1904 [kpc]    H0inv=13.7
    # top_level_cell       = 0.0952 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    
    'map_r'           : {'arcsec':0.1895, 'kpc':1.1427 },
    'map_e'           : {'arcsec':0.1973, 'kpc':1.1904 },
}
'''
scales['ASW0000h2m'][7024] = {
    # Pixel radius         = 12
    # Map radius           = 0.2149 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2238 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0179 [arcsec]
    # Map radius           = 1.2962 [kpc]    H0inv=13.7
    # Map Extent           = 1.3502 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1080 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    
    'map_r'           : {'arcsec':0.2149, 'kpc':1.2962 },
    'map_e'           : {'arcsec':0.2238, 'kpc':1.3502 },
}
'''
scales['ASW0000h2m'][7025] = {
    # Pixel radius         = 12
    # Map radius           = 0.2135 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2224 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0178 [arcsec]
    # Map radius           = 1.2876 [kpc]    H0inv=13.7
    # Map Extent           = 1.3413 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1073 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0

    'map_r'           : {'arcsec':0.2135, 'kpc':1.2876 },
    'map_e'           : {'arcsec':0.2224, 'kpc':1.3413 },
}





# copy paste output from systems/many2.py and manualy select appropriate
levels = {

    'ASW0001hpf':[
        #-16.142110, # 0, canc
        -16.141714, # 1, sad
        #-16.361394, # 2, sad
        -14.334876, # 3, sad
        #-16.592044, # 4, min
        #-19.762615, # 5, min
        #-0.101102, # 6, max
    ],

    'ASW0002z6f':[
        -162.471264, # 0, sad
        #-172.294899, # 1, sad
        #-184.197987, # 2, min
        #-116.410651, # 3, max
    ],

    'ASW0000vqg':[
        #-190.133668, # 0, sad
        #345.775218, # 1, sad
        -238.205802, # 2, sad
        #-276.154188, # 3, min
        #-221.944628, # 4, max
    ],

    'ASW000102p':[
        -21.963930, # 0, sad
        #-60.054127, # 1, min
        #1.977912, # 2, max
    ],

    'ASW000195x':[
        -682.197488, # 0, sad
        #-812.917806, # 1, min
        #-643.822578, # 2, max
    ],

    'ASW0004oux':[
        -174.988464, # 0, sad
        -159.098235, # 1, sad
        #-177.867092, # 2, min
        #-178.550062, # 3, min
        #-125.416518, # 4, max
    ],

    'ASW0000h2m':[
        #-44.048133, # 0, sad
        #-44.044997, # 1, canc
        -44.044446, # 2, canc
        #-44.046207, # 3, canc
        #-44.049515, # 4, canc
        #-44.452050, # 5, sad
        #-48.079721, # 6, sad
        -39.369070, # 7, sad
        #-44.839509, # 8, min
        #-48.080767, # 9, min
        #-0.206511, # 10, max
    ],


}


def test():
#  for idd, elem in enumerate(spg.data):
#    mid = elem['id']
#    draw_mod(0, mid, 0, spg.data, spg.sims)
#    break
  for asw in many.sim:
    draw_sim(asw, many.sim)
    break


def plot_sel():
# only plot selected plots, no tex output
  sel_sim_plots()
  sel_mod_plots()
  plotAllRE()

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
#   generate only selected sim plots
#==============================================================================
def sel_sim_plots():
  print '\nSIMS'
  print '============================================='  
  iii=0
  for asw in many.sim:
    if not asw in sel_sim:
        continue
    else:
        iii=iii+1
        print iii,'/',len(sel_sim)
    path = os.path.join(simdir, asw)
    if not os.path.isdir(path):
      os.makedirs(path)    
    
    get_sim_adv_data(asw)
    draw_sim(asw, many.sim)
    #if debug: break    

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
#   # generate only used models plots
#==============================================================================
def sel_mod_plots():
  print '\nMODS'
  print '============================================='  
  iii=0
  for idd, elem in enumerate(spg.data):
    
    mid = elem['id']
    
    if not mid in sel_mod:
      print mid
      continue
    else:
        iii=iii+1
        print iii,'/',len(sel_mod)

    path = os.path.join(moddir, '%06i'%mid)
    if not os.path.isdir(path):
      os.makedirs(path)    

    get_mod_adv_data(mid) #download plots generated on server with glass
    draw_mod(mid, elem, spg.data, spg.sims)

    #if debug: break
  

#==============================================================================
#   
# fetch online only used models plots
#==============================================================================
def fetch_sel_mod():
  print '\nMODS (fetching only)'
  print '============================================='  
  iii=0
  for idd, elem in enumerate(spg.data):
    
    mid = elem['id']
    
    if not mid in sel_mod:
      print mid
      continue
    else:
        iii=iii+1
        print iii,'/',len(sel_mod)

    path = os.path.join(moddir, '%06i'%mid)
    if not os.path.isdir(path):
      os.makedirs(path)    

    get_mod_adv_data(mid) #download plots generated on server with glass
  
  
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
  filt_imgs = []
  for i, ext in enumerate(exts):
    filt_imgs[i] = [_ for _ in imgs if _.endswith('.%s'%ext)]
  imgs = []
  for fis in filt_imgs:
    imgs.extend(fis)
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

  copied=[]
  for f in files:
    for ext in exts:
      if f.endswith('.%s'%ext):
        try:
          shutil.copy2(os.path.join(imgpath,f), figpath)
          copied.append(f)
        except:
          print '!! file not found:', os.path.join(imgpath,f)
        print '.',

  print ' ...DONE.'
  for f in copied: print '  - %s'%f
  return True
    

def get_mod_def_data(mid):
  """gets the deault data directly from mite web"""
  '''
  baseurl = 'http://mite.physik.uzh.ch/result/%06i/' %mid
  
  imgs = ['img2.png', 'img3.png']
  saveas = ['mass.png', 'arr_time.png']
  
  # box to cut
  x=71
  y=61
  dd=477

  box_mod = (x,y,x+dd,y+dd)

  path = os.path.join(moddir, '%06i'%mid)

  for k, img in enumerate(imgs):
    r = rq.get(baseurl+img, stream=True)
    if r.status_code == 200:
      with open(os.path.join(path, 'tmp.png'), 'wb') as f:
        for chunk in r.iter_content(1024):
          f.write(chunk)
          
      with open(os.path.join(path, 'tmp.png'), 'rb') as f:
        oimg = PIL.Image.open()
        nimg = oimg.crop(box_mod)
        nimg.save(os.path.join(path, saveas[k]))
    
  os.remove(os.path.join(path, 'tmp.png'))
  '''        


def get_mod_adv_data(mid):
  """gets the better plots produced by script"""
  print '> getting model data online', 
  
  if not fetch_onlinedata:
    print "SKIPPING (check fetch_onlinedata)"
    return
  
  baseurl = 'http://mite.physik.uzh.ch/script_output/gen_plots_for_paper/%06i/' %mid
  
  ext = 'png' # server only serves png files...
  
  imgs = ['img1', 'img2', 'img3']
  saveas_ = ['spaghetti', 'mass', 'arr_time']

  # box to cut
  x=171
  y=61
  dd=477
  box_mod = (x,y,x+dd,y+dd)

  #append eextension
  imgs = [_+'.%s'%ext for _ in imgs]
  saveas = ['org_%06i_%s.%s'%(mid, _, ext) for _ in saveas_]
  saveas2 = ['square_%06i_%s.%s'%(mid, _, ext) for _ in saveas_]
  saveas3 = ['clear_%06i_%s.%s'%(mid, _, ext) for _ in saveas_]
  saveas3 = ['%06i_%s.%s'%(mid, _, ext) for _ in saveas_]
  
  #path = os.path.join(moddir, '%06i'%mid)
  path = os.path.join(moddir)

  for k, img in enumerate(imgs):
    r = rq.get(baseurl+img, stream=True)
    if r.status_code == 200:
      with open(os.path.join(path, saveas[k]), 'wb') as f:
        for chunk in r.iter_content(1024):
          f.write(chunk)
          
      # this cuts away any border
      with open(os.path.join(path, saveas[k]), 'rb') as f:
        oimg = PIL.Image.open(f)
        nimg = oimg.crop(box_mod)
        nimg.save(os.path.join(path, saveas3[k]))

    else:
      print '!! file', baseurl, img, 'not found'

  try:
    os.remove(os.path.join(path, 'tmp.png'))
  except:
    pass

      
  # get input image
  r = rq.get('http://mite.physik.uzh.ch/result/%06i/input.png'%mid, stream=True)
  if r.status_code == 200:
    with open(os.path.join(path, '%06i_%s.%s'%(mid, 'input', ext)), 'wb') as f:
      for chunk in r.iter_content(1024):
        f.write(chunk)
  else:
    print '!! file input.png not found'
  
  print '...DONE.'
  for f in saveas: print '  - %s'%f
  print '  - input.png'
  
  # cut images to square borders
  from PIL import Image
  for j, iname in enumerate(saveas):
    im = Image.open(os.path.join(path, iname))
    w,h = im.size
    b = (w-h)/2
    im.crop((b, 0, w-b, h)).save(os.path.join(path, saveas2[j]))
    print '  -',saveas2[j]
  


def get_sim_adv_data(asw):
  """gets some online data"""
  print '> getting sims data online', 
  
  if not fetch_onlinedata:
    print "SKIPPING (check fetch_onlinedata)"
    return

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
    print '!!! ERROR WHILE FETCHING DATA'
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
    
    #path = os.path.join(simdir, asw)
    #if not os.path.isdir(path):
    #  os.makedirs(path)  
    
    #prevent submodules prints..
    if not debug:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        devnull = open(os.devnull, 'w')
        sys.stdout = devnull
        #sys.stderr = devnull
      
    print asw
    
    
    if debug:
        N = 50
        #,R = 20,50   #used to be 100
        print "!! using lowres grid since debug is on"
    else:
        N,R = 200,50   #used to be 100
    
    if sim[asw][0] == 'quasar':
        flag,R = 'Q',20
    if sim[asw][0] == 'galaxy':
        flag,R = 'G',20
    if sim[asw][0] == 'cluster':
        flag,R = 'C',50

    # for the moment, just use some random dict entry from scales[asw]
    #map_ext=scales[asw].itervalues().next()['map_e']['arcsec']
    #R = map_ext * div_scale_factors
    
    for modid in scales[asw].keys():
    
        path = os.path.join(simdir, '%s_%06i' % (asw, modid))
        print "   making plots for %s with scales from %06i" % (asw, modid)
    
        map_ext=scales[asw][modid]['map_e']['arcsec']
        R = map_ext * div_scale_factors

        print map_ext
        print R

        x = np.linspace(-R,R,N)
        y = 1*x
        kappa,arriv = many.grids(asw,x,y)


        #
        # KAPPA - MASS MAP
        #
        if simplots['kappa']:
            print '::: plot mass map'
            mpl.rcParams['contour.negative_linestyle'] = 'dashed'
            fig = pl.figure(figsize=figsize)
            panel = fig.add_subplot(1,1,1)
            panel.set_aspect('equal')
            
            #lev = np.linspace(0,10,41)
            #pc = panel.contour(x,y,kappa,lev, colors=0.8)

            eps = 1e-15 #small offset to prevent div/0 in log()
            
            # kappa(x,y) is value at (x,y), but pcolormesh needs edge coordinates of patches
            # kappa(xi, yj) => x[i]-d / y[j]-d ... x[i+1]-d / y[j+1]-d ; with d step/cell width
            d=2.*R/(N-1)
            x_cm=np.linspace(-R-d/2.,R+d/2.,N+1)
            y_cm=1.*x_cm
            
            # cut border of 0 pixels, delete rrr rows on each side
            rr=2
            kappa_cut = kappa[rr:-rr,rr:-rr]
            x_cut=x[rr:-rr] #original x,y will be used later
            y_cut=y[rr:-rr] 
            x_cm=x_cm[rr:-rr] #x_cm not, just overwrite
            y_cm=y_cm[rr:-rr]
            
            n_contours=15
            
            pc = panel.contour(x_cut,y_cut, 2.5*np.log10(kappa_cut+eps), n_contours, colors='0.9' )
            
            #panel.clabel(pc, inline=1, fontsize=10)
            panel.pcolormesh(x_cm, y_cm, np.log10(kappa_cut+eps), vmin=np.log10(eps), vmax=np.log10(np.amax(kappa_cut)), edgecolors="None", cmap='bone', shading="flat")
            
            panel.tick_params(
                axis='both',       # changes apply to the x- and y-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                left='off',        # ticks along the bottom edge are off
                right='off',       # ticks along the top edge are off
                labelbottom='off',
                labeltop='off',
                labelleft='off',
                labelright='off'
                )
                
            #panel.set_xlim([-R,R])
            #panel.set_ylim([-R,R])
            
            #pl.savefig(os.path.join(path, '%s.%s'%(filenames[1],ext)))
            #pl.savefig(os.path.join(path + '_%s.%s'%(filenames[1],'pdf')))
            #pl.savefig(os.path.join(path + '_%s.%s'%(filenames[1],'png')))
            for ext in exts:
              p = os.path.join(path + '_%s.%s'%(filenames[1],ext))
              pl.savefig(p, bbox_inches='tight', pad_inches=0)
              print '  - %s'%p

            pl.clf() #close current figure
            
            
        #
        # KAPPA ENCLOSED
        #
        if simplots['kappaenc']:
            fig = pl.figure(figsize=figsize)
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
            #pl.savefig(os.path.join(path, '%s.%s'%(filenames[2],ext)))
            #pl.savefig(os.path.join(path + '_%s.%s'%(filenames[2],'png')))
            #pl.savefig(os.path.join(path + '_%s.%s'%(filenames[2],'pdf')))
            for ext in exts:
              p = os.path.join(path + '_%s.%s'%(filenames[2],ext))
              pl.savefig(p)
              print '  - %s'%p
            
            pl.clf() #close current figure
            
        #
        # ARRIVAL TIME CONTOUR PLOT
        #
        if simplots['arriv']:
            fig = pl.figure(figsize=figsize)
            panel = fig.add_subplot(1,1,1, axisbg='white')
            panel.set_aspect('equal')
            lo,hi = np.amin(arriv), np.amax(arriv)
            lev = np.linspace(lo,lo+.2*(hi-lo),30)
            
            mpl.rcParams['contour.negative_linestyle'] = 'solid'
            #panel.contour(x,y,arriv,lev, cmap=mpl.cm.gist_rainbow, linewidths=3)
            panel.contour(x,y,arriv,lev, colors='magenta', linewidths=2)
            panel.contour(x,y,arriv,levels[asw], colors='black', linewidths=4)

            
            # hide axis
            panel.axes.get_xaxis().set_ticks([])
            panel.axes.get_yaxis().set_ticks([])
            
            for ext in exts:
              p = os.path.join(path + '_%s.%s'%(filenames[0],ext))
              pl.savefig(p, bbox_inches='tight', pad_inches=0)
              print '  - %s'%p
          
            pl.clf() #close current figure
    
    
    if not debug:
        #restore stdout
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    print '...DONE.'
    #for f in filenames: print '  - %s'%(f+'.'+repr(exts))


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
  
  yvals_extr = np.logspace(np.log10(3.5),np.log10(1),8)
  ypos_theta = np.logspace(np.log10(7),np.log10(5),4)
  
  # text offsets and properties
  t_dx = 0.0
  t_dy = 0.1
  t_dt = mmax/16.
  t_props = {'ha':'left', 'va':'bottom', 'fontsize':params['text.fontsize']} 
    
    
  pl.ioff()
  fig = pl.figure(figsize=figsizeKE)
  ax = fig.add_subplot(1,1,1)
  
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
    #pl.plot([p['d'], p['d']], [0.01,ofs-t_dt*jj], c+':')
    #pl.text(p['d']+t_dx, ofs-t_dt*jj+t_dy, p['t'], **t_props)
    
    # new placement in logscales
    pl.plot([p['d'], p['d']], [0.01,yvals_extr[jj]], c+':')
    pl.text(p['d']+t_dx, yvals_extr[jj], p['t'], **t_props)

  # plot simulation parameter data
  pl.plot(sims[name]['x'], sims[name]['y'], 'r')
  pl.plot([0.01,np.max(elem['x'])], [1,1], ':m')  
  
  #titles etc
  pl.suptitle('Analysis for ID: %s - model of: %s' % (elem['id'], name), fontsize=18)
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

    #pl.plot(a_re_mean, [0.001,rE_pos], '--', color=(0,0.5,0))
    #pl.text(rE_mean+t_dx, rE_pos+t_dy, r'$\Theta _\text{E}$ = %4.2f'%(rE_mean), **t_props)
    
    #new placement due to logscale
    pl.plot(a_re_mean, [0.001,ypos_theta[2]], '--', color=(0,0.5,0))
    pl.text(rE_mean+t_dx, ypos_theta[2], r'$\Theta _\text{E}$ = %4.2f'%(rE_mean), **t_props)
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
    
    #pl.plot(a_re_data, [0.001,rE_pos+t_dt], '--r')
    #pl.text(rE_data+t_dx, rE_pos+t_dt+t_dy, r'$\Theta_\text{E,sim}$ = %4.2f'%(rE_data), **t_props)
    # new placement due to log scale
    pl.plot(a_re_data, [0.001,ypos_theta[0]], '--r')
    pl.text(rE_data+t_dx, ypos_theta[0], r'$\Theta_\text{E,sim}$ = %4.2f'%(rE_data), **t_props)
    

  
  
  pl.xlabel(r'image radius [pixels]')
  pl.ylabel(r'mean convergance [1]')  
  
  pl.xlim([0,np.max(elem['x'])])
  pl.ylim([0.4,10])

  #ax = pl.gca()
  #pl.text(0.95, 0.95,elem['name'],
  #  horizontalalignment='right',
  #  verticalalignment='top',
  #  fontsize=14,
  #  transform = ax.transAxes)

  ax.set_yscale('log')
  
  if show:
    #print 'show'
    pl.show()
  else:
    #imgname = ('kappa_encl.%s'%ext)
    #pl.savefig(os.path.join(save_fig_path, imgname))
    
    # new style direct image names \figs_new\mod\001234_kappa_encl.ext
    # save as png and pdf anyways
    imgname = ('_kappa_encl.%s'%repr(exts)) #only for debug message print on screen

    for ext in exts:
      imgname1 = ('_kappa_encl.%s'%ext)
      pl.savefig(os.path.join(save_fig_path + imgname1))
    pass
  
  
  print ' ... DONE.'
  print '  - %s' % imgname

  
  
tmp={}
def plotAllRE():
  '''plots the final big scatter plot with all rE'''
  print '> drawing EinsteinR plots',

  import gen_table as tab

  tab.read()  
  
  path = resdir
  if not os.path.isdir(path):
    os.makedirs(path)    

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
  ac = [] # accepted and not rejected?
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

    ac.append(tab.all_mods[str(dat['id'])]['acc'])
    
  xi = np.array(xi)
  re = np.array(re)
  ep = np.array(ep) - re
  em = re - np.array(em)
  ee = [ep, em]
  re_rel = np.array(re_rel)
  ep_rel = np.array(ep_rel) - re_rel
  em_rel = re_rel - np.array(em_rel)
  ee_rel = [ep_rel, em_rel]

  ac = np.array(ac, dtype=bool)
  
  if ERplots[0]:
    pl.figure(figsize=figsizeER)
    #paint accepted
    pl.errorbar(xi[ac], re[ac], [ep[ac], em[ac]], marker='s', mfc='blue', ls='' ,ecolor='blue')
    #paint rejected
    pl.errorbar(xi[~ac], re[~ac], [ep[~ac], em[~ac]], marker='o', mfc='green', ls='' ,ecolor='green')
    pl.plot(xi, se, 'rx')
    pl.xlim([np.min(xi), np.max(xi)])
    pl.ylim([0., 35.])
    pl.xlabel('model id')
    pl.ylabel(r'Einstrin radius $\Theta_\text{E}$ [pixel]')
    
    for ext in exts:
      pl.savefig(os.path.join(path, 'eR_1.'+ext))
    print '.',
    #pl.show()
  
  if ERplots[1]:  
    pl.figure(figsize=figsizeER)
    pl.errorbar(xi, re_rel, ee_rel, marker='s', mfc='blue', ls='' ,ecolor='blue')
    pl.plot(xi, xi*0+1, '-r')
    
    for ext in exts:
      pl.savefig(os.path.join(path, 'eR_2.'+ext))
    print '.',
    #pl.show()
  
  if ERplots[2]:
    pl.figure(figsize=figsizeER)
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

    for ext in exts:
      pl.savefig(os.path.join(path, 'eR_3.'+ext))
    print '.',
    #pl.show()
    
  if ERplots[3]:
    pl.figure(figsize=figsizeER)
    for i, dat in enumerate(spg.data):
      simn = dat['name']    
      try:
        lu[simn]
      except KeyError:
        continue
      if dat['user']=='psaha':
        style = 'rx'
      elif not tab.all_mods[str(dat['id'])]['acc']:
        style = 'g+'
      else:
        style = 'bx'
      xofs = 0.15 if dat['user']=='psaha' else -0.15
      pl.plot(lu[simn]+xofs, dat['rE_mean']/sims[simn], style)
      
    lbls = [key for key, val in spg.sims.items()]
    for i, item in enumerate(spg.sims.items()):
      key, val = item
    pl.plot([-0.5, i+0.5], [1,1], '--r')
    
    pl.xticks(range(i+1), lbls, rotation=90)
    pl.yticks(np.linspace(0,2,(2/0.25)+1))
    pl.grid(axis='y')
    pl.gcf().subplots_adjust(bottom=0.25)
    pl.xlim([-.5, i+0.5])
    pl.xlabel('Simulation id')
    pl.ylabel(r'rel Einstein Radius $\Theta_{\text{E}}$/$\Theta_{\text{E, sim}}$')

    for ext in exts:
      pl.savefig(os.path.join(path, 'eR_4.'+ext))
    print '.',
    #pl.show()
  
  mod_err = getModelError()
  
  if ERplots[4]:
    fig = pl.figure(figsize=figsizeER)
    ax = fig.add_subplot(1,1,1)
    
    draw_later = []
    draw_later2 = []
    flag = ''    
    new_data = []
    for i, dat in enumerate(spg.data):
      simn = dat['name']    
      skip = False
      try:
        lu[simn]
      except KeyError:
        continue
      style = 'wo'
      if dat['user']=='psaha':
        style = 'bo'
        #skip=True
        draw_later.append([sims[simn], dat['rE_mean']])
        flag = "expert"
      elif not tab.all_mods[str(dat['id'])]['acc']:
        style = 'g+'
        flag = "rejected"
      elif mod_err[dat['id']]['anyerr']:
        style = 'bx'
        draw_later2.append([sims[simn], dat['rE_mean']])
        flag = "imgrecon wrong"
      else:
        style = 'wo'
        flag = "good"
      #xofs = 0.15 if dat['user']=='psaha' else -0.15
      #ax.plot(lu[simn]+xofs, dat['rE_mean']/sims[simn], style)
      ax.plot(sims[simn], dat['rE_mean'], style, markersize=4)
      new_data.append((sims[simn], dat['rE_mean'], flag))
    
    with open("new_data.csv", "w") as f:
        for d in new_data:
            f.write("%f,%f,%s\n" % d)
    ddd = 0.5
    for d in draw_later:
      #pass
      ax.plot(d[0], d[1], 'co', markersize=4)
      #ax.arrow(d[0]+ddd, d[1]-ddd, -ddd, ddd, fc="k", ec="k", head_width=0.3, head_length=0.2, length_includes_head=True, zorder=1000)

    for d in draw_later2:
      ax.plot(d[0], d[1], 'bx', markersize=4)
    
      
    lbls = [key for key, val in spg.sims.items()]
    for i, item in enumerate(spg.sims.items()):
      key, val = item
    
    ax.plot([0.1, 100], [0.1,100], 'm:')
    #ax.plot([1, 100], [2,200], 'm')
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    from matplotlib.ticker import LogFormatter, ScalarFormatter
    
    #ax.xaxis.set_minor_formatter(LogFormatter(labelOnlyBase=False))
    ax.xaxis.set_major_formatter(LogFormatter(labelOnlyBase=False))
    ax.xaxis.set_minor_formatter(LogFormatter(labelOnlyBase=False))
    ax.yaxis.set_major_formatter(LogFormatter(labelOnlyBase=False))
    ax.yaxis.set_minor_formatter(LogFormatter(labelOnlyBase=False))
    
    #pl.xticks(range(i+1), lbls, rotation=90)
    #pl.yticks(np.linspace(0,2,(2/0.25)+1))
    #pl.grid(axis='y')
    #pl.gcf().subplots_adjust(bottom=0.25)
    pl.xlim([4, 25])
    pl.ylim([1, 40])
    pl.xlabel(r'actual Einstein Radius $\log(\Theta_{\text{E, act}})$')
    pl.ylabel(r'recovered Einstein Radius $\log(\Theta_{\text{E, rec}})$')

    
    for ext in exts:
      pl.savefig(os.path.join(path, 'eR_5.'+ext))
    print '.',
    #pl.show()
    

    
  print ' ... DONE'


def getModelError():
    #print 'getting error data'
    import csv
    
    err_path = os.path.abspath(os.path.join(pardir, 'spaghetti/data/mod_chal/overview.csv'))
    #err_data = np.loadtxt(err_path, delimiter = ',')
    #print 'errpath:', err_path
    err_data = {}
    with open(err_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            try:
                #print row[1], row[20], 
                modnr=int(row[1])
                err5 = (str(row[20]) == 'x')
                err6 = (str(row[21]) == 'x')
                err_data[modnr] = {
                    'anyerr': err5 or err6,
                    'err5'  : err5,
                    'err6'  : err6,
                }
                #print modnr, err5, err6, err5 or err6
            except StandardError as e:
                #print e
                pass
    return err_data
    
  
if __name__ == "__main__":
  #sel_sim_plots()
  pass
  
  