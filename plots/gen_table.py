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


inp_file_name = 'overview.csv'
inp_file_path = '../spaghetti/data/mod_chal'

out_file_name = 'results.tex'
out_file_path = '../text/tab/auto'

inpfile = os.path.join(os.path.abspath(inp_file_path),inp_file_name)
outfile = os.path.join(os.path.abspath(out_file_path),out_file_name)


all_data = {}
all_stats = []

with open(inpfile, 'r') as f:
  csvr = csv.reader(f)
  
  simname = ''

  for i, row in enumerate(csvr):
    #print row

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
  
    if i<2 or i>155 or (row[0]=='' and row[1]==''):
      continue
    
    if row[0]!='':
      #print row[0]
      simname=row[0]
      all_data[simname]=[]
      
    else:
      if simname=='ASW0001gae':
        continue
      #print row[1], row[29], row[30], row[31]

      r12 = reduce(lambda x, y: x+y, [Frac(_) for _ in row[12].split(' ') if _!='']).limit_denominator()
      r13 = reduce(lambda x, y: x+y, [Frac(_) for _ in row[13].split(' ') if _!='']).limit_denominator()

      #true / false values / strings
      t = "X"
      f = 'O'

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
      
      a = row[16:26]
      #print a
      a = [_=='x' for _ in a]
      #print a
      
      s=[]
      for j, l in enumerate(a):
        if l:
          s.append(str(j+1))
          
      er = ','.join(s)
      data['errors'] = er
      
      #print data
      all_data[simname].append(data)


texstr = ''


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



tex_rowh_tmpl = r'''
      \multicolumn{6}{l}{%s}\\
      \hline
'''

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


############################################

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



texstr += tex_head_tmpl
for simname, data in all_data.items():
  #print simname#, data
  texstr += tex_rowh_tmpl % simname
  s_tbl = s_tbl_head
  for d in data:
    if not d['use']:
      continue
    #print d
    #print tex_row_tmpl % d
    texstr += tex_row_tmpl % d
    s_tbl += tex_row_tmpl % d
  s_tbl += s_tbl_foot % {
    'capt': 'Bblablabla '+simname,
    'lbl' : simname,
  }
  path = os.path.join(os.path.abspath(out_file_path), simname+'.tex')
  with open(path, 'w') as stex:
    stex.write(s_tbl)  
  

texstr += tex_foot_tmpl
    
    
with open(outfile, 'w') as tex:
  tex.write(texstr)


tex_stats = r'\begin{table}\centering\begin{tabular}{lcc}\hline'
tex_stats += '\n'
tex_stats += r'value & n & p \\'
tex_stats += '\n'
tex_stats += r'\hline'
tex_stats += '\n'
nn=int(all_stats[1]['n'])
for key, val in all_stats[1].items():
  if key=='err':
    for m, v in enumerate(val):
      tex_stats += r' %s & %s & %.2f\\' % (key+'%2i'%m, v, float(v)/nn)
      tex_stats += '\n'
  elif key=='':
    pass
  else:
    tex_stats += r' %s & %s & %.2f\\' % (key, val, float(val)/nn)
  tex_stats += '\n'
tex_stats += '\n'
tex_stats += r'\end{tabular}\caption{Stats}\label{tab:stats}\end{table}'
path = os.path.join(os.path.abspath(out_file_path), '_stats.tex')
with open(path, 'w') as stex:
  stex.write(tex_stats)  
