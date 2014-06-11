# -*- coding: utf-8 -*-
"""
removes the white border from the SL png images
"""

import numpy as np
from PIL import Image as img



# dim of new imgs
newdim_mod = (box_mod[2]-box_mod[0], box_mod[3]-box_mod[1])


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

sel_mod = [6915]

for i in sel_mod:
    for t in ['arr_time', 'mass']:
        oimg = img.open('%06i_%s.png' % (i,t))
        nimg = oimg.crop(box_mod)
        nimg.save('cropped\\%06i_%s.png' % (i,t))