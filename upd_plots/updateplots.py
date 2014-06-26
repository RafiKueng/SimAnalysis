# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 16:40:04 2014

@author: RafiK
"""

if False: # get rid of undefined variables in ide
  glass_basis = None
  loadstate = None


import matplotlib.pyplot as plt
import os
import sys

# bugfix for interactive mode
if not 'plots' in sys.modules:
  import plots
else:
  reload(plots)

try: # check if glass already loaded (in interactive mode)
  a = loadstate
except:
  glass_basis('glass.basis.pixels', solver=None)



inppath = "states"
outpath = "outp"
exts = ["png"]


files = [(os.path.splitext(_)) for _ in os.listdir(inppath) if not _.startswith('.')]


print "starting.."

for fn, fe in files: # filename fn, fileextension fe
  ifpath = os.path.join(inppath,fn+fe)
  
  print " > working on %s" % fn
  
  state = loadstate(ifpath)
  state.make_ensemble_average()

  fig = plots.new_kappaplot(state.ensemble_average, with_contours=True)

  for ext in exts:
    ofpath = os.path.join(outpath,"Image for %s.%s"%(fn,ext))
    fig.savefig(ofpath, facecolor='black', edgecolor='none')

  plt.close()
  
  print " \--- DONE"