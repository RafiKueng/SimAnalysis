# -*- coding: utf-8 -*-
"""
adds the new improved srcdiff plot plot for a list of ids

needs to be run with glass env variables set
best to source the run_glass file

Created on Mon Aug 19 21:33:21 2013

@author: RafiK
"""

debug = True
brk = True
filename = "" #should contain one id per line



import os
import matplotlib.pylab as pl

glass_basis('glass.basis.pixels', solver=None)
exclude_all_priors()


if debug:
  ids = ['000010']
else:
  with open(filename, 'r') as f:
    ids = f.readlines()
  print ids

for idd in ids:
  if brk: continue
  path = '../tmp_media/%06i/'%int(idd)

  print "ID: %s "%idd,

  if not os.path.exists(path):
    print "path %s not found" % path
    continue

  if os.path.isfile(path+'img3_ipol.png'):
    print "already has ipol img"
    continue

  if os.path.isfile(path+'state.txt'):
    print "statefile exists"
    g = loadstate(path+'state.txt')
    g.make_ensemble_average()
    g.srcdiff_plot_adv(g.ensemble_average, night=True, upsample=8)
    pl.savefig('../tmp_media/%06i/img3_ipol.png'%int(idd), facecolor='black', edgecolor='none')
    pl.close()
    continue

  print 'no statefile. modify cfg.gls and rerun'
  #todo: implement this


