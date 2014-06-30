# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 16:40:04 2014

@author: RafiK
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
np.set_printoptions(precision=3)


def new_kappaplot(model, obj_index=0, **kwargs):
    """basically copied from glass plot.py, but heavily modified"""
    kw = kwargs

    obj, data = model['obj,data'][obj_index]
    if not data: return None

    #with_contours   = kwargs.pop('with_contours', True)
    #only_contours   = kwargs.pop('only_contours', False)
    #label_contours  = kwargs.pop('label_contours', False)
    #clevels         = kwargs.pop('clevels', 30)
    #with_colorbar   = kwargs.pop('with_colorbar', False) # colorbar is nor working
    #vmin            = kwargs.pop('vmin', None)
    #vmax            = kwargs.pop('vmax', None)
    #subtract        = kwargs.pop('subtract', 0)
    #xlabel          = kwargs.pop('xlabel', r'arcsec')
    #ylabel          = kwargs.pop('ylabel', r'arcsec')
    
    #sl scaling factors
    rscale          = kw.pop('rscale', 440./500*100) # default Spacewarps -> SL -> glass scaling of radius
    dist_fact       = kw.pop('dist_fact', 0.428)     # because measurement at different redshiffts (we had 0.5/1 hardcoded in beginning)
    delta           = kw['contour'].pop('cldelta', 0.1) # contour level spacing in log space




    # SET UP DATA

    # fix the different scaling of glass and SL
    R = obj.basis.mapextent
    extent = np.array([-R,R,-R,R]) / rscale

    # prepare data
    grid = obj.basis._to_grid(data['kappa'],1)
    grid *= dist_fact
    grid = np.where(grid==0,np.nan,np.log10(grid))


    ma = np.nanmax(grid)
    mi = np.nanmin(grid)
    ab = ma if ma>-mi else -mi
    clev = np.arange(0,ab+1e-10,delta)
    clevels = np.concatenate((-clev[:0:-1],clev))
    
    print "ma, mi, ab", ma, mi, ab
    print "extent", extent
    np.set_printoptions(precision=3)
    print clevels
    

    # PLOTTING

    # setup
    kw['contour'].setdefault('extent', extent)
#    kw.setdefault('extend', 'both') # contour levels are automatically added to one or both ends of the range so that all data are included
#    #kw.setdefault('interpolation', 'nearest')
#    kw.setdefault('aspect', 'equal')
#    kw.setdefault('origin', 'upper')
#    #kw.setdefault('cmap', cm.bone)
#    kw.setdefault('colors', 'k')
#    kw.setdefault('antialiased', True)

    # plot
    fig = plt.figure(**kw['figure'])
    ax = fig.add_subplot(1,1,1)
    C = ax.contour(grid, levels=clevels, **kw['contour'])
    ax.set_aspect('equal')
    return fig


    '''
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
    '''

    
    '''    
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
    '''

    
    
    
    
    
    
    
    
    
    
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
