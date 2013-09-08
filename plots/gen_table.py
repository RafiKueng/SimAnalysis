# -*- coding: utf-8 -*-
"""
generates the results table.

dataorigin is the overview.csv, which is generated from
overview.ods by saving as csv.

Created on Sun Sep 08 17:05:05 2013

@author: RafiK
"""

import os
import csv
from fractions import Fraction as Frac


#==============================================================================
# SETTINGS
#==============================================================================

inp_file_name = 'overview.csv'
inp_file_path = '../spaghetti/data/mod_chal'

out_file_name = 'results.tex'
out_file_path = '../text/tab/auto'

# for tex template settings see below

#==============================================================================
# PARSING
#==============================================================================

inpfile = os.path.join(os.path.abspath(inp_file_path),inp_file_name)
outfile = os.path.join(os.path.abspath(out_file_path),out_file_name)


all_data = {}
all_stats = []

with open(inpfile, 'r') as f:
  csvr = csv.reader(f)
  
  simname = ''

  for i, row in enumerate(csvr):
    #print row

    # get the stats from the end of the file
    if i in [156,159,162,165]:
      
      all_stats.append({
        'n'          : int(row[ 5]),
        'npnt'       : int(row[ 7]),
        'approxPlace': int(row[ 8]),
        'approx'     : int(row[ 9]),
        'veryRight'  : int(row[10]),
        'rightPlace' : int(row[12]),
        'rightType'  : int(row[13]),
        'rightOrder' : int(row[14]),
        'err'        : [int(_) for _ in row[16:26]]
      })

    # skip if not in data rows  
    if i<2 or i>155 or (row[0]=='' and row[1]==''):
      continue
    
    
    if row[0]!='': # if header row containing sim name
      #print row[0]
      simname=row[0]
      all_data[simname]=[]
      
    else: # regular data
      if simname=='ASW0001gae': # we don't like this sim
        continue

      # recover the fractions in row 12 and 13 as such..
      # makes sure strings like '2/3', '1 3/5' ect are recovered as math. fractions/numbers
      r12 = reduce(lambda x, y: x+y, [Frac(_) for _ in row[12].split(' ') if _!='']).limit_denominator()
      r13 = reduce(lambda x, y: x+y, [Frac(_) for _ in row[13].split(' ') if _!='']).limit_denominator()

      #true / false values / strings in output
      t = "X"
      f = 'O'

      # read rows
      data = {
        'id'         : row[1],
        'npnt'       : t if row[ 7]=='x' else f,
        'approxPlace': t if row[ 8]=='1' else f,
        'approx'     : t if row[ 9]=='1' else f,
        'veryRight'  : t if row[10]=='1' else f,
        'rightPlace' : r12,
        'rightType'  : r13,
        'rightOrder' : t if row[14]=='1' else f,
        'errors'     : '',
        'use'        : True if row[29]=='1' else False,
        'fav1'       : True if row[30]=='1' else False,
        'fav2'       : True if row[31]=='1' else False,
      }
      
      # parse the errors into a string of error number
      a = row[16:26]
      a = [_=='x' for _ in a] # list of bools
      s=[] # list of strings with err id
      for j, l in enumerate(a):
        if l:
          s.append(str(j+1))
      er = ','.join(s) #final string ,-sep ids
      data['errors'] = er
      
      all_data[simname].append(data)



#==============================================================================
# LONG ALL INCL TABLE SETTINGS / TEMPLATE
#==============================================================================

# caption
ca = '''1. col: places of imgs idendited correctly; 2. col: more or less
correct identification of extr points. 3.col: exact identification of extremal
points. 4.col: type(s) of errors ocured....
1) innacurate in arc
2) min-sad conf in 3 img.
3) only 3 imgs instead 5
4) arc not expanded ()
5) PI-err (rot by 180deg, 2 saddle points false)
6) PI/2-err (rot by 90deg, sad->min->sad->min->sad)
7) missed faint image(s)
8) missed double img(s)
9) too many imgs
'''


settings = {
  'layout': 'p{1cm} l c c c c',
  'capt': ca,
  'lbl' : 'Label',
}
      

#tex_head_tmpl = r'''
#\begin{table}
#  \centering
#    \begin{tabular}{%(layout)s}
#''' % {
#  'layout': 'p{1cm} l c c c c'
#}

tex_head_tmpl = r'''
\begin{center}
  \begin{longtable}{%(layout)s}
''' % settings


# sim header row
tex_rowh_tmpl = r'''
      \multicolumn{6}{l}{%s}\\
      \hline
'''

#regular row
tex_row_tmpl  = r'''      & %(id)s & %(approxPlace)s & %(approx)s & %(veryRight)s & %(errors)s\\
'''


#tex_foot_tmpl = r'''
#    \end{tabular}
#    \caption{%(capt)s}
#    \label{tab:%(lbl)s}
#\end{table}
#''' % {
#  'capt': 'Caption',
#  'lbl' : 'Label'
#    }

tex_foot_tmpl = r'''
    \caption{%(capt)s}
    \label{tab:%(lbl)s}
    \end{longtable}
\end{center}
''' % settings


#==============================================================================
# ONE TABLE PER SIM TABLESETTINGS / TEMPLATE
#==============================================================================

s_settings = settings

s_tbl_head = r'''
\begin{table}
  \centering
    \begin{tabular}{%(layout)s}
''' % s_settings

s_tbl_foot = r'''
    \end{tabular}
    \caption{%(capt)s}
    \label{tab:%(lbl)s}
\end{table}
'''


#==============================================================================
# THE TEX GENERATION
#==============================================================================

texstr = ''
texstr += tex_head_tmpl
for simname, data in all_data.items():

  texstr += tex_rowh_tmpl % simname   # create section header for long table
  s_tbl = s_tbl_head # create table header for short table

  # collect data
  for d in data:
    if not d['use']: #skip if it's marked not to be used in spread sheet
      continue
    
    texstr += tex_row_tmpl % d #make tex string for long table
    s_tbl += tex_row_tmpl % d  #make tex string for short table

  # generate table footer for short table
  s_tbl += s_tbl_foot % {
    'capt': 'Bblablabla '+simname,
    'lbl' : simname,
  }
  
  #.. and save short table
  path = os.path.join(os.path.abspath(out_file_path), simname+'.tex')
  with open(path, 'w') as stex:
    stex.write(s_tbl)  
  
# gen footer for lang table
texstr += tex_foot_tmpl

# ...and save it    
with open(outfile, 'w') as tex:
  tex.write(texstr)


#==============================================================================
# THE CUMMULATED STATUS TABLE
#==============================================================================

# gen header
tex_stats = r'\begin{table}\centering\begin{tabular}{lcc}\hline'
tex_stats += '\n'
tex_stats += r'value & n & p \\'
tex_stats += '\n'
tex_stats += r'\hline'
tex_stats += '\n'

# get number of samples (for % calc)
nn=int(all_stats[1]['n'])

for key, val in all_stats[1].items():
  if key=='err': # split up errors
    for m, v in enumerate(val):
      tex_stats += r' %s & %s & %.2f\\' % (key+'%2i'%m, v, float(v)/nn)
      tex_stats += '\n'

  elif key=='': # should not happend...
    pass
  
  else: # normal case
    tex_stats += r' %s & %s & %.2f\\' % (key, val, float(val)/nn)

  tex_stats += '\n'

# table footer
tex_stats += '\n'
tex_stats += r'\end{tabular}\caption{Stats}\label{tab:stats}\end{table}'

# ... and save
path = os.path.join(os.path.abspath(out_file_path), '_stats.tex')
with open(path, 'w') as stex:
  stex.write(tex_stats)  
