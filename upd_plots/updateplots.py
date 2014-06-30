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

np.set_printoptions(precision=3)

try: # check if glass already loaded (in interactive mode)
  a = loadstate
except:
  glass_basis('glass.basis.pixels', solver=None)
  

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self  
  
  


figargs = AttrDict({
    'figsize'   : (8,8),  # size in inches
    'dpi'       : 80,       #
    'facecolor' : 'w',
    'edgecolor' : 'k',
})

contourargs = AttrDict({
    'extend'        : 'both', # contour levels are automatically added to one or both ends of the range so that all data are included
    'aspect'        : 'equal',
    'origin'        : 'upper',
    'colors'        : 'k',
    'antialiased'   : True,
    'cldelta'       : 0.05, # contour level spacing in log space
})

savefigargs = AttrDict({
    'dpi'       : figargs.dpi
})


kw = AttrDict({'figure': figargs, 'contour': contourargs, 'savefig': savefigargs,})




inppath = "states"
outpath = "outp"
outfn = "Image for %(fname)s.%(ext)s"
exts = ["png",'pdf']

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


files = [(os.path.splitext(_)) for _ in os.listdir(inppath) if not _.startswith('.')]


print "starting.."

for fn, fe in files: # filename fn, fileextension fe
    kw.fname = fn
    kw.fext  = fe 
    ifpath = os.path.join(inppath,fn+fe)
      
    print " > working on %s" % fn
      
    state = loadstate(ifpath)
    state.make_ensemble_average()
    
    fig = plots.new_kappaplot(state.ensemble_average, **kw)
    
    for ext in exts:
        kw.ext = ext
        ofpath = os.path.join(outpath,outfn%kw)
        #fig.savefig(ofpath, facecolor='black', edgecolor='none')
        fig.savefig(ofpath, **kw.savefig)
    
        plt.close()
      
    print " \--- DONE"
    #break
  


def downloadstates():
    
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
