# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from PIL import Image as img

fact = 750./480

org_dim = np.array([600,480,70,50,60,60])
new_dim = np.int16(np.round(org_dim * fact))

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

#sel_mod = [6915]

for mnr in sel_mod:
    nimg = img.new(img.MODES[6], (new_dim[0],new_dim[0]), color=(255,255,255))
    
    oimg = img.open('inputs\\%06i.png' % mnr)
    
    nimg.paste(oimg, (new_dim[2], new_dim[4], 750+new_dim[2],750+new_dim[4]))
    nimg.save('new_inputs\\%06i_input_old.png' % mnr)
    
    #set source and target
    src = oimg    
    trg = img.new(img.MODES[6], src.size, color=(255,255,255))
    trg.paste(src, (0, 0, src.size[0],src.size[1]))
    srcpix = src.load()
    trgpix = trg.load()
    sx, sy = src.size
    
    #kernel = [(-1,0),(0,-1),(1,0),(0,1)]
    kernel = [  (-1, 0),( 0,-1),( 1, 0),( 0, 1),
                (-1,-1),(-1,+1),(+1,-1),(+1,+1)]
    
    lernel = [
    [ 0.0 , 0.2 , 0.5 , 0.2 , 0.0],
    [ 0.2 , 0.8 , 1.0 , 0.8 , 0.2],
    [ 0.5 , 1.0 , 1.0 , 1.0 , 0.5],
    [ 0.2 , 0.8 , 1.0 , 0.8 , 0.2],
    [ 0.0 , 0.2 , 0.5 , 0.2 , 0.0],
    ]
    
    #lernel = [[1.0]]
    
    kernel = []
    d=len(lernel)//2
    for i, r in enumerate(lernel):
        for j, a in enumerate(r):
            kernel.append((i-d, j-d, a))
    
    cr, cg, cb = (255,0,255)
    for x in range(sx):
        for y in range(sy):
            #print pix[x,y]
            r,g,b = srcpix[x,y]
            if r==255 and g==0 and b==255:
                for dx, dy, aa in kernel:
                    bb = 1.-aa
                    aa=bb=0.5
                    try:
                        r,g,b = srcpix[x+dx,y+dy]
                    except Exception as e:
                        #print "error", x, y, dx, dy, e
                        continue
                    nc = (int(aa*cr+bb*r),int(aa*cg+bb*g),int(aa*cb+bb*b))
                    #print nc
                    trgpix[x+dx,y+dy] = nc
                
    trg.save('new_inputs\\%06i_input.png' % mnr)
