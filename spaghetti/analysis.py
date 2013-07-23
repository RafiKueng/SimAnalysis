
'''
how to run this file?

first export the env variables needed (see run_glass)

then:
python glass.py analysis.py

'''

from __future__ import division

import os
import re

import pylab as pl
from pylab import show, figure, ion, ioff, savefig, gcf
from math import pi, cos
import numpy as np
from numpy import zeros
from itertools import izip

import csv

#switch of using tex to plot
from matplotlib import rc
rc('text', usetex=False)


#os.environ['LD_LIBRARY_PATH'] = '/win/proj/master/glassMint/build/glpk_build/lib'

glass_basis('glass.basis.pixels', solver=None)
exclude_all_priors()


data_dir = '../../SimAnalysis/spaghetti/demodata'
data_dir = '/srv/lmt/tmp_media'
data_dir = os.path.abspath(data_dir)


files  = [
  '002784','002787','002792','002794','002798','002782','002801','002860',
  '002870','002872','002891','002895','002904','002964','002972','003851',
  '002980','002996','003004','003034','003204','003211','003243','003250',
  '003262','003270','003350','003353','003378','003380','003388','002903',
  '002903','003150','003347','003301','003170','003186','003405','003408',
  '003450','003451','003454','003469','003510','003530','003537','003542',
  '003560','003596','003604','003642','003649','003782','003783','003802',
  '003932',
  #2nd page
  '003417','003419','003440','003673','003495','003579','003661','003681',
  '003692','003706','003834','003714','003733','003874','003889','003895',
  '003897','003916','003925','003926','003943'
  ]

# i've gotten the filenames with:
# re.findall('mite\.physik\.uzh\.ch\/data\/(\d+)', txt)
# in the html source
  
  
auth_re = re.compile('meta\(author=\'(.*)\',')
inf_re = re.compile('globject\(\'(\d+)__(.+)\'')

  
distance_factor = 0.428
div_scale_factors = 440./500*100

#output file
filen = open('/home/rafik/data.csv', 'w')

csvfilen = csv.writer(filen)
#file0 = open('kappaR_enc.csv', 'w')
#csvfile0 = csv.writer(file0)
#file1 = open('kappaR_enc_err_p.csv', 'w')
#csvfile1 = csv.writer(file0)
#file2 = open('kappaR_enc_err_m.csv', 'w')
#csvfile2 = csv.writer(file0)
  
for iii, fl in enumerate(files):
  print 'file %3i / %3i' % (iii, len(files))

  fstr = os.path.join(data_dir, fl, 'state.txt')
  g = loadstate(fstr)

  g.make_ensemble_average()
  obj,data=g.ensemble_average['obj,data'][0]
  
  n_rings = len(obj.basis.rings) # number of rings with center (=pixrad+1)
  
  #print n_rings
  
  kappaRenc_median = np.zeros(n_rings) #pixrad
  kappaRd_encl = np.zeros(n_rings) #pixrad
  kappaRenc_1sigmaplus = np.zeros(n_rings) #pixrad
  kappaRenc_1sigmaminus = np.zeros(n_rings) #pixrad
  kappaRd_maxdevplus = np.zeros(n_rings) #pixrad
  kappaRd_maxdevminus = np.zeros(n_rings) #pixrad
  
  pixPerRing = np.zeros(n_rings)
  pixEnc = np.zeros(n_rings)
  
  for i in range(n_rings):
    pixEnc[i] = len(obj.basis.rings[i])
    pixPerRing[i] = len(obj.basis.rings[i])
    for j in range(i):
      pixEnc[i] += len(obj.basis.rings[j])

  for k in range(n_rings): #pixrad
    kappaRenc_k_all = np.zeros(0)
    for m in g.models:
      obj,ps = m['obj,data'][0]

      kappaRenc_model = ps['kappa(R)'][k]*pixPerRing[k]
      for kk in range(k):
        kappaRenc_model += ps['kappa(R)'][kk] * pixPerRing[kk]
      kappaRenc_k_all = np.append(kappaRenc_k_all,kappaRenc_model)

    kappaRenc_k_all /= pixEnc[k]
    kappaRenc_k_all *= distance_factor
    
    kappaRenc_k_all = np.sort(kappaRenc_k_all)
    #print kappaRenc_k_all
    #print len(kappaRenc_k_all), pixEnc[k]
    
    kappaRenc_median[k] = kappaRenc_k_all[len(kappaRenc_k_all)/2]
#    kappaRenc_1sigmaplus[k] = kappaRenc_k_all[5*len(kappaRenc_k_all)/6]
#    kappaRenc_1sigmaminus[k] = kappaRenc_k_all[len(kappaRenc_k_all)/6]
    p = 0.05
    kappaRenc_1sigmaplus[k] = kappaRenc_k_all[int((1.0-p)*len(kappaRenc_k_all))]
    kappaRenc_1sigmaminus[k] = kappaRenc_k_all[int(p*len(kappaRenc_k_all))]
    
    #print k, kappaRenc_median[k], kappaRenc_1sigmaplus[k], kappaRenc_1sigmaminus[k]





  pixelradius = n_rings -1

  kappaRd_median = zeros(pixelradius+1) #pixrad
  kappaRd_1sigmaplus = zeros(pixelradius+1) #pixrad
  kappaRd_1sigmaminus = zeros(pixelradius+1) #pixrad
  kappaRd_maxdevplus = zeros(pixelradius+1) #pixrad
  kappaRd_maxdevminus = zeros(pixelradius+1) #pixrad
  
  for k in range(pixelradius+1): #pixrad
    kappaRd_k_all = zeros(0)
    for m in g.models:
      obj,ps = m['obj,data'][0]
      kappaRd_model = ps['kappa(R)'][k]#-kappaRs[k]
      kappaRd_k_all = np.append(kappaRd_k_all,kappaRd_model)
    kappaRd_k_all = np.sort(kappaRd_k_all)
    kappaRd_median[k] = kappaRd_k_all[len(kappaRd_k_all)/2]
    kappaRd_1sigmaplus[k] = kappaRd_k_all[5*len(kappaRd_k_all)/6]
    kappaRd_1sigmaminus[k] = kappaRd_k_all[len(kappaRd_k_all)/6]
    kappaRd_maxdevplus[k] = kappaRd_k_all[-1]
    kappaRd_maxdevminus[k] = kappaRd_k_all[0]


  
  #pl.plot(np.arange(n_rings), kappaRd_median)
  yerr=[kappaRenc_1sigmaplus - kappaRenc_median, kappaRenc_median- kappaRenc_1sigmaminus]
  
  x_vals = (np.arange(n_rings)+0.5) * div_scale_factors * obj.basis.cell_size[0]
  
  #pl.errorbar(x_vals, kappaRenc_median, yerr=yerr)
  #pl.show()



  yerr=[kappaRd_1sigmaplus - kappaRd_median, kappaRd_median- kappaRd_1sigmaminus]
  
  #pl.errorbar(np.arange(n_rings), kappaRd_median, yerr=yerr)
  #pl.show()
  
  
  with open(os.path.join(data_dir, fl, 'cfg.gls'), 'r') as df:
    txt = df.read()
    try:
      author = auth_re.search(txt).groups()[0]
      name = inf_re.search(txt).groups()[1]
    except:
      author = ''
      name = ''

  print '  > done: ', fl, author, name
  csvfilen.writerow([fl, author, name, len(x_vals)] + list(x_vals) + list(kappaRenc_median) + list(kappaRenc_1sigmaplus) + list(kappaRenc_1sigmaminus))
  #csvfile0.writerow(kappaRenc_median)
  #csvfile1.writerow(kappaRenc_1sigmaplus)
  #csvfile2.writerow(kappaRenc_1sigmaminus)
  
  
  
for f in [filen]:
  f.close()
