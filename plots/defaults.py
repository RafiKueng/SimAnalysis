# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 15:31:20 2014

@author: RafiK
"""
import matplotlib as mpl
from copy import deepcopy

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
def copyAD(ad):
    return AttrDict(deepcopy(ad))


# First programm specific values direclty in args
args = AttrDict({
    'exts'      : ['png', 'pdf'],
    'sel_mods'  : [6915,6919,6937,6941,6975,6990,7020,7021,7022,7024,7025,],
    'sel_sims'  : [
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


#
# MATPLOTLIB RC file defaults - overwrite
# this overwrites de defaults of mpl defined in the rc files
#
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


#
# DEFAULT ATTRIBUTES FOR PLT COMMANDS:
#

args.figure = AttrDict({
    'figsize'   : (8,6),    # w,h tuple in inches
    'dpi'       : 300,       # Dots per inch
    'facecolor' : 'w',      # The figure patch facecolor; defaults to rc figure.facecolor
    'edgecolor' : 'k',      # The figure patch edge color; defaults to rc figure.edgecolor
#    'linewidth' : 1,        # The figure patch edge linewidth; the default linewidth of the frame
#    'frameon'   : True,     # If False, suppress drawing the figure frame
#    'subplotpars' : None,   # A SubplotParams instance, defaults to rc
#    'tight_layout'  : True  # If False use subplotpars; if True adjust subplot parameters using tight_layout() with default padding. When providing a dict containing the keys pad, w_pad, h_pad and rect, the default tight_layout() paddings will be overridden. Defaults to rc figure.autolayout.
})


args.add_subplot = AttrDict({
# http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure.add_subplot
#adjustable 	[ ‘box’ | ‘datalim’ | ‘box-forced’]
#agg_filter 	unknown
#alpha 	float (0.0 transparent through 1.0 opaque)
#anchor 	unknown
#animated 	[True | False]
#aspect 	unknown
#autoscale_on 	unknown
#autoscalex_on 	unknown
#autoscaley_on 	unknown
#axes 	an Axes instance
#axes_locator 	unknown
#axis_bgcolor 	any matplotlib color - see colors()
#axisbelow 	[ True | False ]
#clip_box 	a matplotlib.transforms.Bbox instance
#clip_on 	[True | False]
#clip_path 	[ (Path, Transform) | Patch | None ]
#color_cycle 	unknown
#contains 	a callable function
#figure 	unknown
#frame_on 	[ True | False ]
#gid 	an id string
#label 	string or anything printable with ‘%s’ conversion.
#lod 	[True | False]
#navigate 	[ True | False ]
#navigate_mode 	unknown
#path_effects 	unknown
#picker 	[None|float|boolean|callable]
#position 	unknown
#rasterization_zorder 	unknown
#rasterized 	[True | False | None]
#sketch_params 	unknown
#snap 	unknown
#title 	unknown
#transform 	Transform instance
#url 	a url string
#visible 	[True | False]
#xbound 	unknown
#xlabel 	unknown
#xlim 	length 2 sequence of floats
#xmargin 	unknown
#xscale 	[‘linear’ | ‘log’ | ‘symlog’]
#xticklabels 	sequence of strings
#xticks 	sequence of floats
#ybound 	unknown
#ylabel 	unknown
#ylim 	length 2 sequence of floats
#ymargin 	unknown
#yscale 	[‘linear’ | ‘log’ | ‘symlog’]
#yticklabels 	sequence of strings
#yticks 	sequence of floats
#zorder 	any number
})


args.plot = AttrDict({
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot

#agg_filter 	unknown
#alpha 	float (0.0 transparent through 1.0 opaque)
#animated 	[True | False]
#antialiased or aa 	[True | False]
#axes 	an Axes instance
#clip_box 	a matplotlib.transforms.Bbox instance
#clip_on 	[True | False]
#clip_path 	[ (Path, Transform) | Patch | None ]
#color or c 	any matplotlib color
#contains 	a callable function
#dash_capstyle 	[‘butt’ | ‘round’ | ‘projecting’]
#dash_joinstyle 	[‘miter’ | ‘round’ | ‘bevel’]
#dashes 	sequence of on/off ink in points
#drawstyle 	[‘default’ | ‘steps’ | ‘steps-pre’ | ‘steps-mid’ | ‘steps-post’]
#figure 	a matplotlib.figure.Figure instance
#fillstyle 	[‘full’ | ‘left’ | ‘right’ | ‘bottom’ | ‘top’ | ‘none’]
#gid 	an id string
#label 	string or anything printable with ‘%s’ conversion.
#linestyle or ls 	['-' | '--' | '-.' | ':' | 'None' | ' ' | ''] and any drawstyle in combination with a linestyle, e.g., 'steps--'.
#linewidth or lw 	float value in points
#lod 	[True | False]
#marker 	unknown
#markeredgecolor or mec 	any matplotlib color
#markeredgewidth or mew 	float value in points
#markerfacecolor or mfc 	any matplotlib color
#markerfacecoloralt or mfcalt 	any matplotlib color
#markersize or ms 	float
#markevery 	None | integer | (startind, stride)
#path_effects 	unknown
#picker 	float distance in points or callable pick function fn(artist, event)
#pickradius 	float distance in points
#rasterized 	[True | False | None]
#sketch_params 	unknown
#snap 	unknown
#solid_capstyle 	[‘butt’ | ‘round’ | ‘projecting’]
#solid_joinstyle 	[‘miter’ | ‘round’ | ‘bevel’]
#transform 	a matplotlib.transforms.Transform instance
#url 	a url string
#visible 	[True | False]
#xdata 	1D array
#ydata 	1D array
#zorder 	any number

})


args.savefig = AttrDict({
# http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.savefig
    'dpi'           : args.figure.dpi,
    'facecolor'     : args.figure.facecolor,
    'edgecolor'     : args.figure.edgecolor,
#    'transparent'   : False,    # If True, the axes patches will all be transparent; the figure patch will also be transparent unless facecolor and/or edgecolor are specified via kwargs 
#    'frameon'       : True,     # If True, the figure patch will be colored, if False, the figure background will be transparent.
#    'bbox_inches'   : 'tight',  # Bbox in inches. Only the given portion of the figure is saved. If ‘tight’, try to figure out the tight bbox of the figure.
#    'pad_inches'    : 0,        # Amount of padding around the figure when bbox_inches is ‘tight’.
})


# putting together the default plot style
#args = AttrDict()

args.default = AttrDict()
args.default.figure    = args.figure
args.default.addsub    = args.add_subplot
args.default.plot      = args.plot
args.default.savefig   = args.savefig


#
# TEMPLATES
#  template styles to overwrite default plotting styles
#
tmpl = AttrDict()

# square figure format 
tmpl.squares = copyAD(args.default)
tmpl.squares.figure.update({
    'figsize'   : (8,8),
})
tmpl.squares.addsub.update({
    'aspect'   : 'equal',
})
tmpl.squares.savefig.update({
    'bbox_inches'   : 'tight',  # Bbox in inches. Only the given portion of the figure is saved. If ‘tight’, try to figure out the tight bbox of the figure.
    'pad_inches'    : 0,        # Amount of padding around the figure when bbox_inches is ‘tight’.
})
tmpl.squares.contour = AttrDict({
    'extend'        : 'both', # contour levels are automatically added to one or both ends of the range so that all data are included
    'aspect'        : 'equal',
    'origin'        : 'upper',
    'colors'        : 'k',
    'antialiased'   : True,
})

# the others have default values
tmpl.rects = copyAD(args.default)


# Formatter Functions

def remove_all_ticks(fig=None, axes=None, lines=None):
    axes.tick_params(
        axis='both',       # changes apply to the x- and y-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        left='off',        # ticks along the bottom edge are off
        right='off',       # ticks along the top edge are off
        labelbottom='off',
        labeltop='off',
        labelleft='off',
        labelright='off'
        )
    return
    
    
def detailed_log_capt(fig=None, axes=None, lines=None):
    from matplotlib.ticker import LogFormatter
    axes.xaxis.set_major_formatter(LogFormatter(labelOnlyBase=False))
    axes.xaxis.set_minor_formatter(LogFormatter(labelOnlyBase=False))
    axes.yaxis.set_major_formatter(LogFormatter(labelOnlyBase=False))
    axes.yaxis.set_minor_formatter(LogFormatter(labelOnlyBase=False))
    return


#collect the formatter
args.formatter = AttrDict({
    'removeticks'   :   remove_all_ticks,
#    'removeticks'   :   lambda axes: None,
    'detailed_log_capt' : detailed_log_capt,   
})


#
# INDIVIDUAL PLOTS / STYLES DEFINITIONS
#
#

args.kappa = copyAD(tmpl.squares)
args.kappa.update({
    'cldelta'       : 0.1, # contour level spacing in log space
    'rmnrow'        : 1 # remove n rows for kappa plot
})
args.kappa.formatter = remove_all_ticks


# arrivtime
args.arriv = copyAD(tmpl.squares)
args.arriv.update({
    'nlev'  : 30,
    'rangef': 0.8,
})
args.arriv.majorc = copyAD(tmpl.squares.contour)
args.arriv.majorc.update({
    'colors'    : 'black',
    'linewidths': 4,
    'linestyles': 'solid',
})
args.arriv.minorc = copyAD(tmpl.squares.contour)
args.arriv.minorc.update({
    'colors'    : 'magenta',
#    'linewidths': 2, #use default
    'linestyles': 'solid',
})


# kappa enclosed for models
args.kappaenc = copyAD(tmpl.rects)
args.kappaenc.addsub.update({
    'yscale'    : 'log',
})
args.kappaenc.update({
    'model'     : AttrDict({'color': 'blue'}),
    'modelface' : AttrDict({'facecolor': 'blue', 'alpha': 0.5}),
    'sim'       : AttrDict({'color': 'red' }),
    'min'       : AttrDict({'color': 'black' , 'linestyle':':' }),
    'max'       : AttrDict({'color': 'black'  , 'linestyle':':' }),
    'sad'       : AttrDict({'color': 'black', 'linestyle':':' }),
    'text'      : AttrDict({'ha': 'left', 'va':'bottom' }),
    'unity'     : AttrDict({'color': 'black' , 'linestyle':':' }),

    'rEmod'     : AttrDict({'color': 'blue' , 'linestyle':'--' }),
    'rEsim'     : AttrDict({'color': 'red' ,       'linestyle':'--' }),
})


# final plot with the einstein radii
args.eR4 = copyAD(tmpl.rects)
args.eR4.addsub.update({
    'xscale'    : 'log',
    'yscale'    : 'log',
})

markersize = 4

args.eR4.update({
    'expert'        : AttrDict({
        'color'     :'blue',
        'marker'    :'o',
        'markerfacecolor': 'cyan',
        'markersize': markersize
        }),

    'rejected'      : AttrDict({
        'color'     :'green',
        'marker'    :'+',
#        'markerfacecolor': 'green',
        'markersize': markersize
        }),

    'regular'       : AttrDict({
        'color'     :'black',
        'marker'    :'o',
        'markerfacecolor': 'white',
        'markersize': markersize
        }),

    'failed'        : AttrDict({
        'color'     :'blue',
        'marker'    :'x',
#        'markerfacecolor': 'white',
        'markersize': markersize
        }),

    'unity'     : AttrDict({
        'color': 'black' ,
        'linestyle':':'
    }),
})


def set_mpl():
    #mpl.rcParams.update(args.mplrc)
    for k, v in args.mplrc.items():
        if type(v)==dict:
            mpl.rc(k, **v)
        else:
            mpl.rcParams[k] = v
