# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 20:16:55 2014

@author: RafiK
"""

import sys, os
import glob
from PIL import Image as img

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import scales
#import defaults


outdir = "out"


SSR    = 2048. # pixel dimensions of screen shot
GLSSCL =  100. # scaling from glass to SL 
SWPX   =  440. # width of sw image
SLPX   =  500. # width of a sl image



def find_center(img, color=(255,0,0)):
    szx, szy = img.size    
    px = img.load()
    cr, cg, cb = color
    
    mx, my = (0,0)
    n = 0
    
    for x in range(szx):
        for y in range(szy):
            r,g,b,a = px[x,y]
            
            if cr==r and cg==g and cb==b:
                #print x,y
                mx += x
                my += y
                n += 1
    #print "med:", mx/n, my/n
    
    m = (mx/n, my/n)
    #return map(lambda x: int(round(x)), m)
    return m


for imgname in glob.glob("*.png"):
    imgn = imgname[:-4]
    mid, scale = imgn.split('_')
    mid = int(mid)
    scale = float(scale)
    
    print mid, scale
    
    #nimg = img.new(img.MODES[6], (new_dim,new_dim), color=(255,255,255))
    oimg = img.open(imgname)
    opix = oimg.load()
    
    mx, my = find_center(oimg)
    mape = scales.sc2[mid]
    
    # half height of new image (based on the map extent)
    hsz = mape * GLSSCL * SSR * SWPX * scale / SLPX / SWPX
    
    
    box = (mx-hsz, my-hsz, mx+hsz, my+hsz)
    box = map(lambda x: int(round(x)), box)

    print (mx, my), hsz, box
    
    nimg = oimg.crop(box)
    #nimg.show()
    nimg.save("%s/%06i_input.png" % (outdir, mid))
    
    #oimg.resize(newsize, img.ANTIALIAS)
