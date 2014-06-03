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

for i in sel_mod:
    nimg = img.new(img.MODES[6], (new_dim[0],new_dim[0]), color=(255,255,255))
    oimg = img.open('new_inputs\\%06i.png' % i)
    
    nimg.paste(oimg, (new_dim[2], new_dim[4], 750+new_dim[2],750+new_dim[4]))
    
    nimg.save('new_inputs\\%06i_input.png' % i)