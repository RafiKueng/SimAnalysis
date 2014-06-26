# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 16:40:04 2014

@author: RafiK
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np


def new_kappaplot(model, obj_index=0, **kwargs):
    """basically copied from glass plot.py, but heavily modified"""
  
    obj, data = model['obj,data'][obj_index]
    if not data: return

    with_contours   = kwargs.pop('with_contours', False)
    only_contours   = kwargs.pop('only_contours', False)
    label_contours  = kwargs.pop('label_contours', False)
    clevels         = kwargs.pop('clevels', 30)
    with_colorbar   = kwargs.pop('with_colorbar', False) # colorbar is nor working
    vmin            = kwargs.pop('vmin', None)
    vmax            = kwargs.pop('vmax', None)
    subtract        = kwargs.pop('subtract', 0)
    xlabel          = kwargs.pop('xlabel', r'arcsec')
    ylabel          = kwargs.pop('ylabel', r'arcsec')
    



    R = obj.basis.mapextent
    kw = default_kw(R, kwargs)


    grid = obj.basis._to_grid(data['kappa']-subtract,1)
    if vmin is None:
        w = data['kappa'] != 0
        if not np.any(w):
            vmin = -15
            grid += 10**vmin
        else:
            vmin = np.log10(np.amin(data['kappa'][w]))
        #print 'min?', np.amin(data['kappa'] != 0)
        kw.setdefault('vmin', vmin)

    if vmax is not None:
        kw.setdefault('vmax', vmax)

    grid = np.log10(grid.copy()) # + 1e-15)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    if not only_contours:
        #pl.matshow(np.log10(grid), **kw)
        ax.matshow(grid, **kw)
        #imshow(grid, fignum=False, **kw)
        #pl.matshow(grid, fignum=False, **kw)
        if with_colorbar: 
            glscolorbar()

    if only_contours or with_contours:
        #if 'colors' in kw and 'cmap' in kw:
            #kw.pop('cmap')

        kw.setdefault('colors', 'w')
        kw.setdefault('extend', 'both')
        kw.setdefault('alpha', 0.7)
        kw.pop('cmap')
        #kw.pop('colors')
        C = plt.contour(grid, clevels, **kw)
        if label_contours:
            ax.clabel(C, inline=1, fontsize=10)
        plt.gca().set_aspect('equal')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    return fig
    
    
    
    
    
    
    
    
    
    
#
# HELPERS directly taken from glass/plots.py
#    
    
def glscolorbar():
    rows,cols,_ = plt.gca().get_geometry()
    x,y = plt.gcf().get_size_inches()
    pars = plt.gcf().subplotpars
    left = pars.left
    right = pars.right
    bottom = pars.bottom
    top = pars.top
    wspace = x*pars.wspace
    hspace = y*pars.hspace
    totWidth = x*(right-left)
    totHeight = y*(top-bottom)

    figH = (totHeight-(hspace*(rows>1))) / rows
    figW = (totWidth-(wspace*(cols>1))) / cols

    plt.colorbar(plt.gcf(), shrink=figW/figH)
    
    
def default_kw(R, kw={}):
    kw.setdefault('extent', [-R,R,-R,R])
    kw.setdefault('interpolation', 'nearest')
    kw.setdefault('aspect', 'equal')
    kw.setdefault('origin', 'upper')
    #kw.setdefault('fignum', False)
    kw.setdefault('cmap', cm.bone)
    #if vmin is not None: kw['vmin'] = vmin
    #if vmax is not None: kw['vmax'] = vmax
    return kw
