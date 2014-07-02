# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 15:31:20 2014

@author: RafiK
"""
import matplotlib as mpl

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


args = AttrDict({
    'exts'      : ['png', 'pdf'],
    'sel_mods'  : [6915,6919,6937,6941,6975,6990,7020,7021,7022,7024,7025,],
    'sel_sim'   : [
        'ASW000102p',
        'ASW000195x',
        'ASW0000vqg',
        'ASW0004oux',
        'ASW0001hpf',
        'ASW0000h2m',
        'ASW0002z6f',
        ],

    'rscale'    : 440./500*100, # default Spacewarps -> SL -> glass scaling of radius
    'dist_fact' : 0.428,        # because measurement at different redshiffts (we had 0.5/1 hardcoded in beginning)


})



args.figure = AttrDict({
    'figsize'   : (8,6),  # size in inches
    'dpi'       : 80,       #
    'facecolor' : 'w',
    'edgecolor' : 'k',
})


args.squarefig = AttrDict(args.figure)
args.squarefig.update({
    'figsize'   : (8,8),
})



args.contour = AttrDict({
    'extend'        : 'both', # contour levels are automatically added to one or both ends of the range so that all data are included
    'aspect'        : 'equal',
    'origin'        : 'upper',
    'colors'        : 'k',
    'antialiased'   : True,
    'cldelta'       : 0.05, # contour level spacing in log space
})

args.savefig = AttrDict({
    'dpi'       : args.figure.dpi,
})


args.mplrc = AttrDict({
    # see http://matplotlib.org/users/customizing.html
    'backend'               : 'agg',
    
    'text'  : {
        #'fontsize'  : 14, # DONT USE, depr.
        'usetex'            : True,
        'latex.preamble'    : [
            r"\usepackage{amsmath}",
            #r"\usepackage{textgreek}",
        ],
    },

    'mathtext.default'      : 'regular',
    
    'font': {
        'family'    :   'serif',
        'size'      :   14,
    },
    
    ('xtick', 'ytick')  : {
        'labelsize' :   12,    
    }


    #'font.family'           : 'serif',

    #'axes.labelsize'        : 14,
    #'legend.fontsize'       : 10,
    #'xtick.labelsize'       : 12,
    #'ytick.labelsize'       : 12,
    #'figure.figsize': fig_size,
    #'axes.unicode_minus': True
})






def set_mpl():
    #mpl.rcParams.update(args.mplrc)
    for k, v in args.mplrc.items():
        if type(v)==dict:
            mpl.rc(k, **v)
        else:
            mpl.rcParams[k] = v
