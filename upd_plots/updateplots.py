# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 16:40:04 2014

@author: RafiK
"""

if False: # get rid of undefined variables in ide
  glass_basis = None
  loadstate = None

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import requests as rq

# bugfix for interactive mode
if not 'plots' in sys.modules:
    import plots
else:
    import plots
    reload(plots)


sys.path.append(os.path.abspath("../plots"))

if not 'defaults' in sys.modules:
    import defaults
else:
    import defaults
    reload(defaults)
    
from defaults import AttrDict
defaults.set_mpl()


np.set_printoptions(precision=3)

try: # check if glass already loaded (in interactive mode)
  a = loadstate
except:
  glass_basis('glass.basis.pixels', solver=None)
  


#class AttrDict(dict):
#    def __init__(self, *args, **kwargs):
#        super(AttrDict, self).__init__(*args, **kwargs)
#        self.__dict__ = self  

  


#figargs = AttrDict({
#    'figsize'   : (8,8),  # size in inches
#    'dpi'       : 80,       #
#    'facecolor' : 'w',
#    'edgecolor' : 'k',
#})
#
#contourargs = AttrDict({
#    'extend'        : 'both', # contour levels are automatically added to one or both ends of the range so that all data are included
#    'aspect'        : 'equal',
#    'origin'        : 'upper',
#    'colors'        : 'k',
#    'antialiased'   : True,
#    'cldelta'       : 0.05, # contour level spacing in log space
#})
#
#savefigargs = AttrDict({
#    'dpi'       : figargs.dpi
#})
#
#
#kw = AttrDict({'figure': figargs, 'contour': contourargs, 'savefig': savefigargs,})


args = defaults.args


inppath = "states"
outpath = "outp"
outfn = "%(name)s_mass.%(ext)s"
exts = args.pop('exts', ['png'])

sel_mod = args.pop('sel_mods', None)


files = [(os.path.splitext(_)) for _ in os.listdir(inppath) if not _.startswith('.')]


print "starting.."

for fn, fe in files: # filename fn, fileextension fe
    args.file = AttrDict({
        'name': fn,
        'oext': fe,
        'path': os.path.join(inppath,fn+fe)
    })
    #args.fname = fn
    #args.fext  = fe 
      
    print " > working on %s" % fn
      
    state = loadstate(args.file.path)
    state.make_ensemble_average()
    
    fig = plots.new_kappaplot(state.ensemble_average, **args)
    
    for ext in exts:
        args.file.ext = ext
        ofpath = os.path.join(outpath,outfn % args.file)
        #fig.savefig(ofpath, facecolor='black', edgecolor='none')
        fig.savefig(ofpath, **args.kappa.savefig)
    
        plt.close()
      
    print " \--- DONE"

  


def downloadstates():
    '''function to run once to fetch all the state files'''
    baseurl = 'http://mite.physik.uzh.ch/result/%(mod)06i/state.txt'
    savepath = './states'
    filename = '%(mod)06i.state'
    
    for mod in sel_mod:
        kw = {'mod':mod}

        print "getting %(mod)06i... [" % kw,
        r = rq.get(baseurl % kw, stream=True)
        i=0
        if r.status_code == 200:
            with open(os.path.join(savepath, filename % kw), 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
                    i+=1
                    if i%1000==0: print '.',
        print '] DONE'
