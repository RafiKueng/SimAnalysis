# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:18:42 2013

@author: rafik
"""

import csv
import numpy as np
import matplotlib.pyplot as plt


sims_dir = '../systems/figs'

user_data_dir = './data.csv'

data = []

# read the user generated data
with open(user_data_dir, 'r') as f:
  csvfile = csv.reader(f)
  
  for row in csvfile:
    l = len(row)

    if l-4 != int(row[3])*4:
      print '!! strange1 error @', row[0], 4*int(row[3]), l-4
      continue
    
    dl = (l-4) / 4  
    
    if (l-4)%4 != 0:
      print '!! strange2 error @', row[0]
      continue 
    
    o = {
      'id':     int(row[0]),
      'user':   row[1],
      'name':   row[2],
      'nr':     row[3],
      'x':      np.array(row[4:4+dl], dtype=float32),
      'y':      np.array(row[4+dl: 4+2*dl], dtype=float32),
      'err_p':  np.array(row[4+2*dl: 4+3*dl], dtype=float32),
      'err_m':  np.array(row[4+3*dl: 4+4*dl], dtype=float32)
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
for elem in data[0:1]:
  name = elem['name']
  
  yerr=[elem['err_p'] - elem['y'], elem['y']- elem['err_m']]

  plt.plot(sims[name]['x'], sims[name]['y'])
  plt.errorbar(elem['x'], elem['y'], yerr=yerr)
  plt.show()