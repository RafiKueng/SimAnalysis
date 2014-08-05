# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 14:22:48 2014

@author: psaha
"""

from numpy import mean, std

full = []
fil = open('new_data.csv')
while True:
    lyne = fil.readline()
    if not lyne:
        break
    full.append(lyne.split(','))

ratio = map(lambda p: [float(p[1])/float(p[0]),p[2]],full)

expert = [p[0] for p in ratio if p[1][:6]=='expert']
good = [p[0] for p in ratio if p[1][:4]=='good']
many = [p[0] for p in ratio if p[1][:6]!='reject']

print len(good), len(ratio), len(expert)
print mean(expert), std(expert)
print mean(many), std(many)
