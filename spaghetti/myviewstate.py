from __future__ import division

glass_basis('glass.basis.pixels', solver=None)
exclude_all_priors()

import os
import pylab as pl
from pylab import show, figure, ion, ioff, savefig, gcf, text, figtext, xticks, twiny
from math import pi, cos
from numpy import matrix, zeros, linspace, sin, cos, pi, sqrt, amax, loadtxt, empty, empty_like, flipud, reshape, repeat, log10, histogram2d
from scipy.linalg import eig, inv
from pylab import arrow, plot, errorbar
from math import acos, floor
from basis.pixels.priors import min_kappa_leier_grid
import numpy as np
import basis.pixels.basis
from glass.scales import convert
from itertools import izip
from basis.pixels.basis import intersect, intersect_frac
import glass.environment
import datetime


def escape(s):
    s = s.replace('_', r'\_')
    return s

def style_iterator(colors='gbrcm'):
    import matplotlib.lines as mpll
    from itertools import count
    _linestyles = [k for k,v, in mpll.lineStyles.iteritems() if not v.endswith('nothing')]
    _linestyles.sort()
    for lw in count(1):
        for ls in _linestyles:
            for clr in colors:
                yield lw,ls,clr

def default_kw(R, kw={}):
    kw.setdefault('extent', [-R,R,-R,R])
    kw.setdefault('interpolation', 'nearest')
    kw.setdefault('aspect', 'equal')
    kw.setdefault('origin', 'upper')
    kw.setdefault('fignum', False)
    return kw


Lscale = 2
Mscale = 1.8e10 
Rcut = 50

just_testing = False
if just_testing:
    produce_subfiles = False
    produce_both_subfiles_and_one_plot = False
    show_plots = True
else:
    produce_subfiles = True
    produce_both_subfiles_and_one_plot = True
    show_plots = False

fig_plot_size = None
fig_nr,fig_nc = None, None 
fig_subplot_index= 1
subfilespath = str()
plot_maxradius_circle = True

leftwidth = .15
rightwidth = .95

def init_plots(size=8, dim=[1,1]): #8 instead of 6
    global fig_plot_size, fig_nr,fig_nc, fig_subplot_index, produce_subfiles, leftwidth, rightwidth
    fig_plot_size = size
    fig_nr,fig_nc = dim
#   fig_subplot_index=1
#   produce_subfiles = with_subfiles
    f = figure(figsize=(fig_plot_size*fig_nc, fig_plot_size*fig_nr))
    f.subplots_adjust(left=leftwidth, right=rightwidth)

def begin_plot():
    global fig_subplot_index, produce_subfiles
    if not produce_subfiles:
        gcf().add_subplot(fig_nr,fig_nc,fig_subplot_index)
    if produce_subfiles:
        init_plots()
    fig_subplot_index += 1

def end_plot():
    global produce_subfiles, subfilespath
    if produce_subfiles:
        tag = '_'+chr(ord('a') + (fig_subplot_index-2))
        savefig('%s%s.eps' % (subfilespath, tag))

def get_xticks_arcsec(max_x,galnum): #bruclaud2012
    tick_values = [0]
    virtual_xvalue = 0
    if galnum == 957:
        while virtual_xvalue < max_x:
            virtual_xvalue += 1.
            tick_values += [virtual_xvalue]
    else:
        while virtual_xvalue < max_x:
            virtual_xvalue += .5
            tick_values += [virtual_xvalue]
    return tick_values


def get_xticks_kpc(max_x_kpc,max_x_arcsec,galnum,dL,nu):
    tick_values = [0]
    tick_labels = [0]

    if galnum == 957:
        virtual_max_kpc = int(floor(max_x_kpc+4))
        virtual_max_arcsec = convert('kpc to arcsec', virtual_max_kpc, dL, nu)
        while virtual_max_arcsec > max_x_arcsec:
            virtual_max_kpc -= 4
            virtual_max_arcsec = convert('kpc to arcsec', virtual_max_kpc, dL, nu)
        virtual_xvalue = 4
        while virtual_xvalue < virtual_max_kpc:
            tick_values += [convert('kpc to arcsec', virtual_xvalue, dL, nu)]
            tick_labels += [virtual_xvalue]
            virtual_xvalue += 4
        tick_values += [virtual_max_arcsec]
        tick_labels += [virtual_max_kpc]

    else:
        virtual_max_kpc = int(floor(max_x_kpc+2))
        virtual_max_arcsec = convert('kpc to arcsec', virtual_max_kpc, dL, nu)
        while virtual_max_arcsec > max_x_arcsec:
            virtual_max_kpc -= 2
            virtual_max_arcsec = convert('kpc to arcsec', virtual_max_kpc, dL, nu)
        virtual_xvalue = 2
        while virtual_xvalue < virtual_max_kpc:
            tick_values += [convert('kpc to arcsec', virtual_xvalue, dL, nu)]
            tick_labels += [virtual_xvalue]
            virtual_xvalue += 2
        tick_values += [virtual_max_arcsec]
        tick_labels += [virtual_max_kpc]

    return tick_values,tick_labels

def get_fig_subplot_index():
    global fig_subplot_index
    return fig_subplot_index

def PlotFigures():
    global fig_subplot_index, subfilespath, fig_nr, fig_nc, fig_plot_size, datatable_still_to_fill, pixelradius, leftwidth, rightwidth

    for g in gls:
        g.make_ensemble_average()
        g.bw_styles = True

    obj,data=g.ensemble_average['obj,data'][0]

    dscale = convert('kappa to Msun/arcsec^2', 1, obj.dL, data['nu'])

    pixelradius = np.shape(obj.basis.rings)[0]-1

    #bruclaud2012: To calculate the maximum radius (radius of the last image)
    maxradius = 0
    for i,src in enumerate(obj.sources):
        for img in src.images:
            temporaryradius = sqrt(img.pos.real**2+img.pos.imag**2)
            if temporaryradius > maxradius: maxradius = temporaryradius

    if not produce_subfiles:
        init_plots(5, [3,4]) #bruclaud2012: Changed; Initially it was: init_plots(4, [2,4])
        gcf().subplots_adjust(left=0.1, right=0.9, hspace = .28, wspace = .25) #bruclaud2012: Changed; Initially it was: gcf().subplots_adjust(left=0.05, right=0.98)
        gcf().suptitle('%s' % escape(os.path.splitext(os.path.basename(opts[1]))[0]))

    titlestring = escape(os.path.splitext(os.path.basename(opts[1]))[0])
    galaxynum = int(titlestring.split('\_')[0])
    galaxynumstring = str(galaxynum)
    while len(galaxynumstring) < 4:
        galaxynumstring = '0'+galaxynumstring
    subfilespath = '/home/ast/read/dark/bruclaud/Plots/'+galaxynumstring+'/'
    subfilespath+= str(datetime.date.today().year*10000+datetime.date.today().month*100+datetime.date.today().day)


    print '1/7' #bruclaud2012


    #for g in gls:
    #   for i,o in enumerate(g.objects):
    #       if hasattr(o, 'stellar_mass'):
    #           g.subtract_kappa_from_models(o.stellar_mass, i, include_ensemble_average=False)


    if 1: 
        begin_plot()
        for g in gls:
#           if 'image' in g.meta_info:
#               R = 20 #g.objects[0].basis.maprad
#               #cx,cy = -1.875, 0.08
#               cx,cy=0,0
#               g.image_plot(g.meta_info['image'], R, [cx,cy])
            g.img_plot(obj_index=0)
            g.arrival_plot(g.ensemble_average, only_contours=True, clevels=30, colors='r');
            g.arrival_plot(g.ensemble_average, only_contours=True, clevels=30, src_index=0, colors='r');
            g.arrival_plot(g.ensemble_average, only_contours=True, clevels=30, src_index=4, colors='g');
            #g.src_plot(obj_index=0)
            #g.src_plot(g.ensemble_average, obj_index=0)
            g.external_mass_plot(0)
        end_plot()

    print '2/7' #bruclaud2012

    if 0:
        for g in gls:
            begin_plot()
            g.kappa_plot(g.ensemble_average, 0, with_contours=True, clevels=20, vmax=1); #Re_plot(env().ensemble_average,0)
            #g.kappa_plot(g.ensemble_average, 0, with_contours=False, vmax=1); #Re_plot(env().ensemble_average,0)
            #g.gradient_plot(g.ensemble_average, 0)
            end_plot()

    if 0:
        for g in gls:
            begin_plot()
            if 'image' in g.meta_info:
                R = 20 #g.objects[0].basis.maprad
                #cx,cy = -1.875, 0.08
                cx,cy=0,0
                g.image_plot(g.meta_info['image'], R, [cx,cy])
            s = 0
            if hasattr(g.objects[0], 'stellar_mass'):
                s = g.objects[0].stellar_mass

            g.kappa_plot(g.ensemble_average, 0, with_contours=True, clevels=20, subtract=s) #, vmax=1, colors='r'); #Re_plot(env().ensemble_average,0)
            #g.kappa_plot(g.ensemble_average, 0, with_contours=False, vmax=1); #Re_plot(env().ensemble_average,0)
            #g.gradient_plot(g.ensemble_average, 0)
            end_plot()

    if 1:
        for g in gls:
            begin_plot()
#           if 'image' in g.meta_info:
#               R = 20 #g.objects[0].basis.maprad
#               #cx,cy = -1.875, 0.08
#               cx,cy=0,0
#               g.image_plot(g.meta_info['image'], R, [cx,cy])
            g.kappa_plot(g.ensemble_average, 0, only_contours=True, clevels=20, colors='k') #'MediumVioletRed') #, vmax=1, colors='r'); #Re_plot(env().ensemble_average,0)
            #g.kappa_plot(g.ensemble_average, 0, with_contours=False, vmax=1); #Re_plot(env().ensemble_average,0)
            #g.gradient_plot(g.ensemble_average, 0)

            if 1: #bruclaud2012: Plots also the eigenvectors and the shape ellipsoid of the total mass distribution
                #Fill a position vector with data only up to the maximum radius maxradius
                r = np.zeros_like(obj.basis.ploc)
                for k in range(pixelradius+1): #pixrad
                    if data['R']['arcsec'][k] > maxradius: break
                    for l in obj.basis.rings[k]:
                        r[l] = obj.basis.ploc[l]

                #First calculate the angles of the averaged model to get a hint where the peak is
                m = data['kappa']
                I=matrix(zeros((2,2)))
                I[0,0]=sum(m*r.imag**2)
                I[0,1]=-sum(m*r.imag*r.real)
                I[1,0]=I[0,1]
                I[1,1]=sum(m*r.real**2)

                V,D=eig(inv(I))
                V1=V[0].real
                V2=V[1].real
                D1=D[:,0]
                D2=D[:,1]

                if abs(V2) > abs(V1):
                    temporary_value = V2.copy()
                    temporary_vector = D2.copy()
                    V2 = V1.copy()
                    D2 = D1.copy()
                    V1 = temporary_value.copy()
                    D1 = temporary_vector.copy()

                theta_avg=acos(D1[0])
                phi_avg=acos(D2[0])
                if D1[1]<0: theta_avg = pi-theta_avg
                if D2[1]<0: phi_avg = pi-phi_avg


                #Calculate all the angles of the total mass models
                theta_all = zeros(0)
                phi_all = zeros(0)
                V1_all = zeros(0)
                V2_all = zeros(0)

                for u in g.models:
                    obj,ps = u['obj,data'][0]
                    kappa_model = ps['kappa']
                    m=kappa_model.copy()

                    I_model=matrix(zeros((2,2)))
                    I_model[0,0]=sum(m*r.imag**2)
                    I_model[0,1]=-sum(m*r.imag*r.real)
                    I_model[1,0]=I_model[0,1]
                    I_model[1,1]=sum(m*r.real**2)

                    V_model,D_model=eig(inv(I_model))
                    V1_model=V_model[0].real
                    V2_model=V_model[1].real
                    D1_model=D_model[:,0]
                    D2_model=D_model[:,1]

                    if abs(V1_model) > abs(V2_model):
                        theta_model=acos(D1_model[0])
                        phi_model=acos(D2_model[0])
                        if D1_model[1]<0: theta_model = pi-theta_model
                        if D2_model[1]<0: phi_model = pi-phi_model
                        V1_all = np.append(V1_all,V1_model)
                        V2_all = np.append(V2_all,V2_model)
                    else:
                        theta_model=acos(D2_model[0])
                        phi_model=acos(D1_model[0])
                        if D2_model[1]<0: theta_model = pi-theta_model
                        if D1_model[1]<0: phi_model = pi-phi_model
                        V1_all = np.append(V1_all,V2_model)
                        V2_all = np.append(V2_all,V1_model)


                    #Here we deal with the fact that angles are pi-periodic in this case and just sorting to find the median is wrong
                    if abs(theta_model-theta_avg)>pi/2:
                        if theta_avg<pi/2: theta_model -= pi
                        else: theta_model += pi
                    if abs(phi_model-phi_avg)>pi/2:
                        if phi_avg<pi/2: phi_model -= pi
                        else: phi_model += pi

                    theta_all = np.append(theta_all,theta_model)
                    phi_all = np.append(phi_all,phi_model)


                #Sort to find the median
                theta_all = np.sort(theta_all)
                phi_all = np.sort(phi_all)
                V1_all = np.sort(V1_all)
                V2_all = np.sort(V2_all)

                theta_median = theta_all[len(theta_all)/2].copy()
                phi_median = phi_all[len(phi_all)/2].copy()
                V1_median = V1_all[len(V1_all)/2].copy()
                V2_median = V2_all[len(V2_all)/2].copy()

                #Now we transform back to have only values between 0 and pi
                if theta_model>pi: theta_model -= pi
                if phi_model>pi: phi_model -= pi

                #Plot the ellipsis
                phispacing = linspace(0,2*pi,1000)

                xcoord = V1_median/V2_median*cos(phispacing)
                ycoord = sin(phispacing)
                xrot = cos(theta_median)*xcoord-sin(theta_median)*ycoord
                yrot = sin(theta_median)*xcoord+cos(theta_median)*ycoord

                #Rescale to fit image size
                resizefactor = obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)/amax((abs(xrot),abs(yrot))) #############################################

                plot(xrot*resizefactor,yrot*resizefactor, color='k',linewidth=1.8)
                arrow(0,0,V1_median/V2_median*cos(theta_median)*resizefactor,V1_median/V2_median*sin(theta_median)*resizefactor, color='k',linewidth=1.8)
                arrow(0,0,cos(theta_median+pi/2)*resizefactor,sin(theta_median+pi/2)*resizefactor, color='k',linewidth=1.8)
                arrow(0,0,-V1_median/V2_median*cos(theta_median)*resizefactor,-V1_median/V2_median*sin(theta_median)*resizefactor, color='k',linewidth=1.8)
                arrow(0,0,-cos(theta_median+pi/2)*resizefactor,-sin(theta_median+pi/2)*resizefactor, color='k',linewidth=1.8)

                if plot_maxradius_circle:
                    circle_x = maxradius*cos(phispacing)
                    circle_y = maxradius*sin(phispacing)
                    plot(circle_x,circle_y,color='r',linewidth=1.5)


                ############################################
                #Same thing, but this time for stellar mass#
                ############################################

                #Enter here galaxy number and the strength of the stellar mass map
                scale = 1.0
                fname = '/home/bruclaud/glass/Examples/StellarMass/'+galaxynumstring+'.dat1'

                if galaxynum == 47: grid_size = .1645*31
                elif galaxynum == 142: grid_size = .2394*31
                elif galaxynum == 414: grid_size = .1755*31
                elif galaxynum == 712: grid_size = .1045*31
                elif galaxynum == 818: grid_size = .2129*31
                elif galaxynum == 911: grid_size = .2897*31
                elif galaxynum == 952: grid_size = .0826*31
                elif galaxynum == 957: grid_size = .3371*31
                elif galaxynum == 1009: grid_size = .1574*31
                elif galaxynum == 1030: grid_size = .1787*31
                elif galaxynum == 1104: grid_size = .2703*31
                elif galaxynum == 1115: grid_size = .1800*31
                elif galaxynum == 1152: grid_size = .1445*31
                elif galaxynum == 1422: grid_size = .1400*31
                elif galaxynum == 1520: grid_size = .1561*31
                elif galaxynum == 1600: grid_size = .1310*31
                elif galaxynum == 1608: grid_size = .1968*31
                elif galaxynum == 2016: grid_size = .3206*31
                elif galaxynum == 2045: grid_size = .1819*31
                elif galaxynum == 2149: grid_size = .1774*31
                elif galaxynum == 2237: grid_size = .1245*31
                else: print 'Something went wrong with the galaxy number!'

                #For 0957
                if galaxynum == 957:
                    if 1: fname = '/home/bruclaud/glass/Examples/StellarMass/0957_square.dat1'
                    elif 0: fname = '/home/bruclaud/glass/Examples/StellarMass/0957_original.dat1'

                print 'Galaxy:',galaxynum
                print 'File name:',fname
                print 'Scale:',scale
                print 'Stellar pixel size:',grid_size/31

                stellardata = loadtxt(fname, skiprows = 2, unpack=True)
                d,c = amax(stellardata[0])+1, amax(stellardata[1])+1
                assert d==c
                grid = stellardata[5] * 1e10 * scale
                grid = grid.reshape((d,c)).T        # Data is stored in column-major order!+
                grid = flipud(grid)

                grid *= (grid_size / grid.shape[0])**2
                a = grid.copy() #a = obj.basis.project_grid(grid, grid_size, H0inv)

                L = obj.basis.pixrad
                S = grid.shape[0]
                J = S // 2

                grid_cell_size = grid_size / S
                cell_size      = obj.basis.top_level_cell_size

                stellar = zeros(len(obj.basis.ploc))
                for idx,[l,cell_size] in enumerate(izip(obj.basis.ploc, obj.basis.cell_size)):
                    x,y = l.real, l.imag
                    rt = y + 0.5*cell_size
                    rb = y - 0.5*cell_size
                    cl = x - 0.5*cell_size
                    cr = x + 0.5*cell_size
                    for i in xrange(2*J+1):
                        for j in xrange(2*J+1):
                            it = (J-i+0.5) * grid_cell_size
                            ib = (J-i-0.5) * grid_cell_size
                            jl = (j-J-0.5) * grid_cell_size
                            jr = (j-J+0.5) * grid_cell_size
                            frac = intersect_frac([rt,rb,cl,cr], [it,ib,jl,jr])
                            stellar[idx] += frac * grid[i,j]

                stellar /= obj.basis.cell_size**2
                stellar /= dscale

                ms=stellar.copy()

                Is=matrix(zeros((2,2)))
                Is[0,0]=sum(ms*r.imag**2)
                Is[0,1]=-sum(ms*r.imag*r.real)
                Is[1,0]=Is[0,1]
                Is[1,1]=sum(ms*r.real**2)

                Vs,Ds=eig(inv(Is))
                V1s=Vs[0].real
                V2s=Vs[1].real
                D1s=Ds[:,0]
                D2s=Ds[:,1]

                if abs(V2s) > abs(V1s):
                    temporary_value = V2s.copy()
                    temporary_vector = D2s.copy()
                    V2s = V1s.copy()
                    D2s = D1s.copy()
                    V1s = temporary_value.copy()
                    D1s = temporary_vector.copy()

                thetas=acos(D1s[0])
                phis=acos(D2s[0])
                if D1s[1]<0: thetas = pi-thetas
                if D2s[1]<0: phis = pi-phis

                phispacing = linspace(0,2*pi,1000)

                xcoord = V1s/V2s*cos(phispacing)
                ycoord = sin(phispacing)
                xrot = cos(thetas)*xcoord-sin(thetas)*ycoord
                yrot = sin(thetas)*xcoord+cos(thetas)*ycoord

                #Rescale to fit image size
                resizefactors = obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)/amax((abs(xrot),abs(yrot))) #############################################

                plot(xrot*resizefactors,yrot*resizefactors, color='c',linewidth=1.8)
                pl.ylim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
                pl.xlim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
                arrow(0,0,V1s/V2s*cos(thetas)*resizefactors,V1s/V2s*sin(thetas)*resizefactors, color='c',linewidth=1.8)
                arrow(0,0,cos(thetas+pi/2)*resizefactors,sin(thetas+pi/2)*resizefactors, color='c',linewidth=1.8)
                arrow(0,0,-V1s/V2s*cos(thetas)*resizefactors,-V1s/V2s*sin(thetas)*resizefactors, color='c',linewidth=1.8)
                arrow(0,0,-cos(thetas+pi/2)*resizefactors,-sin(thetas+pi/2)*resizefactors, color='c',linewidth=1.8)



                #Do a second stellar grid for 0957 using the original prior
                if galaxynum == 957:
                    fnamecopy = '/home/bruclaud/glass/Examples/StellarMass/0957.dat1'
                    stellardatacopy = loadtxt(fnamecopy, skiprows = 2, unpack=True)
                    d,c = amax(stellardatacopy[0])+1, amax(stellardatacopy[1])+1
                    assert d==c
                    grid = stellardatacopy[5] * 1e10 * scale
                    grid = grid.reshape((d,c)).T        # Data is stored in column-major order!+
                    grid = flipud(grid)

                    grid *= (grid_size / grid.shape[0])**2
                    a = grid.copy() #a = obj.basis.project_grid(grid, grid_size, H0inv)

                    L = obj.basis.pixrad
                    S = grid.shape[0]
                    J = S // 2

                    grid_cell_size = grid_size / S
                    cell_size      = obj.basis.top_level_cell_size

                    stellarcopy = zeros(len(obj.basis.ploc))
                    for idx,[l,cell_size] in enumerate(izip(obj.basis.ploc, obj.basis.cell_size)):
                        x,y = l.real, l.imag
                        rt = y + 0.5*cell_size
                        rb = y - 0.5*cell_size
                        cl = x - 0.5*cell_size
                        cr = x + 0.5*cell_size
                        for i in xrange(2*J+1):
                            for j in xrange(2*J+1):
                                it = (J-i+0.5) * grid_cell_size
                                ib = (J-i-0.5) * grid_cell_size
                                jl = (j-J-0.5) * grid_cell_size
                                jr = (j-J+0.5) * grid_cell_size
                                frac = intersect_frac([rt,rb,cl,cr], [it,ib,jl,jr])
                                stellarcopy[idx] += frac * grid[i,j]

                    stellarcopy /= obj.basis.cell_size**2
                    stellarcopy /= dscale

                    mscopy=stellarcopy.copy()


                ##########################################
                #Same Thing but this time for dark matter#
                ##########################################
                dark = data['kappa']-stellar
                if np.any(dark<0): #set equal to zero if stellar mass prior isn't turned on or downscaled too much
                    for k in range(len(obj.basis.ploc)):
                        if dark[k] < 0: dark[k] = 1e-15
                md=dark.copy()

                Id=matrix(zeros((2,2)))
                Id[0,0]=sum(md*r.imag**2)
                Id[0,1]=-sum(md*r.imag*r.real)
                Id[1,0]=Id[0,1]
                Id[1,1]=sum(md*r.real**2)

                Vd,Dd=eig(inv(Id))
                V1d=Vd[0].real
                V2d=Vd[1].real
                D1d=Dd[:,0]
                D2d=Dd[:,1]

                if abs(V2d) > abs(V1d):
                    temporary_value = V2d.copy()
                    temporary_vector = D2d.copy()
                    V2d = V1d.copy()
                    D2d = D1d.copy()
                    V1d = temporary_value.copy()
                    D1d = temporary_vector.copy()

                thetad_avg=acos(D1d[0])
                phid_avg=acos(D2d[0])
                if D1d[1]<0: thetad_avg = pi-thetad_avg
                if D2d[1]<0: phid_avg = pi-phid_avg


                #Calculate all the angles of the dark matter mass models
                thetad_all = zeros(0)
                phid_all = zeros(0)
                V1d_all = zeros(0)
                V2d_all = zeros(0)
                eigvalueratiod_all = zeros(0)

                for u in g.models:
                    obj,ps = u['obj,data'][0]
                    kappa_model = ps['kappa']
                    md=kappa_model.copy()

                    Id_model=matrix(zeros((2,2)))
                    Id_model[0,0]=sum(md*r.imag**2)
                    Id_model[0,1]=-sum(md*r.imag*r.real)
                    Id_model[1,0]=Id_model[0,1]
                    Id_model[1,1]=sum(md*r.real**2)

                    Vd_model,Dd_model=eig(inv(Id_model))
                    V1d_model=Vd_model[0].real
                    V2d_model=Vd_model[1].real
                    D1d_model=Dd_model[:,0]
                    D2d_model=Dd_model[:,1]

                    if abs(V1d_model) > abs(V2d_model):
                        thetad_model=acos(D1d_model[0])
                        phid_model=acos(D2d_model[0])
                        if D1d_model[1]<0: thetad_model = pi-thetad_model
                        if D2_model[1]<0: phid_model = pi-phid_model
                        V1d_all = np.append(V1d_all,V1d_model)
                        V2d_all = np.append(V2d_all,V2d_model)
                        eigvalueratiod_all = np.append(eigvalueratiod_all,V1d_model/V2d_model)
                    else:
                        thetad_model=acos(D2d_model[0])
                        phid_model=acos(D1d_model[0])
                        if D2d_model[1]<0:
                            thetad_model = pi-thetad_model
                        if D1d_model[1]<0:
                            phid_model = pi-phid_model
                        V1d_all = np.append(V1d_all,V2d_model)
                        V2d_all = np.append(V2d_all,V1d_model)
                        eigvalueratiod_all = np.append(eigvalueratiod_all,V2d_model/V1d_model)


                    #Here we deal with the fact that angles are pi-periodic in this case and just sorting to find the median is wrong
                    if abs(thetad_model-thetad_avg)>pi/2:
                        if thetad_avg<pi/2: thetad_model -= pi
                        else: thetad_model += pi
                    if abs(phid_model-phid_avg)>pi/2:
                        if phid_avg<pi/2: phid_model -= pi
                        else: phid_model += pi

                    thetad_all = np.append(thetad_all,thetad_model)
                    phid_all = np.append(phid_all,phid_model)


                #Sort to find the median
                thetad_all = np.sort(thetad_all)
                phid_all = np.sort(phid_all)
                V1d_all = np.sort(V1d_all)
                V2d_all = np.sort(V2d_all)
                eigvalueratiod_all = np.sort(eigvalueratiod_all)

                thetad_median = thetad_all[len(thetad_all)/2].copy()
                phid_median = phid_all[len(phid_all)/2].copy()
                V1d_median = V1d_all[len(V1d_all)/2].copy()
                V2d_median = V2d_all[len(V2d_all)/2].copy()
                eigvalueratiod_median = eigvalueratiod_all[len(eigvalueratiod_all)/2]

                #Now we transform back to have only values between 0 and pi
#                for j in range(len(thetad_all)):                        #took this option out as histogram looks nicer like that
#                    if thetad_all[j]>pi: thetad_all[j] -= pi
#                    if phid_all[j]>pi: phid_all[j] -= pi


                #Plot the ellipsis
                xcoord = V1d_median/V2d_median*cos(phispacing)
                ycoord = sin(phispacing)
                xrot = cos(thetad_median)*xcoord-sin(thetad_median)*ycoord
                yrot = sin(thetad_median)*xcoord+cos(thetad_median)*ycoord

                #Rescale to fit image size
                resizefactord = obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)/amax((abs(xrot),abs(yrot))) #############################################

                plot(xrot*resizefactord,yrot*resizefactord, color='g',linewidth=1.8)
                pl.ylim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
                pl.xlim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
                arrow(0,0,eigvalueratiod_median*cos(thetad_median)*resizefactord,eigvalueratiod_median*sin(thetad_median)*resizefactord, color='g',linewidth=1.8)
                arrow(0,0,cos(thetad_median+pi/2)*resizefactord,sin(thetad_median+pi/2)*resizefactord, color='g',linewidth=1.8)
                arrow(0,0,-eigvalueratiod_median*cos(thetad_median)*resizefactord,-eigvalueratiod_median*sin(thetad_median)*resizefactord, color='g',linewidth=1.8)
                arrow(0,0,-cos(thetad_median+pi/2)*resizefactord,-sin(thetad_median+pi/2)*resizefactord, color='g',linewidth=1.8)


            end_plot()


    print '3/7' #bruclaud2012


    if 1: #bruclaud2012
        begin_plot()
        L = obj.basis.pixrad
        R = obj.basis.mapextent
        refinement = 1
        a = dark.copy()

        bins = (2*L+1)
        X = obj.basis.ploc.real
        Y = -obj.basis.ploc.imag
        gridC = histogram2d(Y, X, bins=bins, weights=a*(obj.basis.int_cell_size==1), range=[[-R,R], [-R,R]])[0]
        gridC *= obj.basis.top_level_cell_size**2

        bins = (2*L+1) * refinement
        gridR = histogram2d(Y, X, bins=bins, weights=a*(obj.basis.int_cell_size!=1)*obj.basis.cell_size**2, range=[[-R,R], [-R,R]])[0]
        grid = gridC + gridR
        grid /= obj.basis.top_level_cell_size**2
        grid = log10(grid.copy())#+1e-4)

        kw = default_kw(R)
        #kw.pop('cmap')
        clevels = 20
        pl.over(pl.contour, grid, clevels, extend='both', colors='g', alpha=.9, **kw)

        if plot_maxradius_circle:
            plot(circle_x,circle_y,color='r',linewidth=1.5)

        pl.gca().set_aspect('equal')
        pl.ylim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
        pl.xlim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
        pl.xlabel(r'$-\Delta\alpha \ \left[\mathrm{arcsec}\right]$')
        pl.ylabel(r'$\Delta\delta \ \left[\mathrm{arcsec}\right]$')

        #1- and 2sigma-arrows
        arrowlengths = zeros(2)
        arrowlengths[0] = eigvalueratiod_median*resizefactord
        arrowlengths[1] = resizefactord

        arrow(0,0,arrowlengths[0]*cos(thetad_median),arrowlengths[0]*sin(thetad_median), color='k',linewidth=1.5)
        arrow(0,0,arrowlengths[1]*cos(thetad_median+pi/2),arrowlengths[1]*sin(thetad_median+pi/2), color='k',linewidth=1.5)
        arrow(0,0,-arrowlengths[0]*cos(thetad_median),-arrowlengths[0]*sin(thetad_median), color='k',linewidth=1.5)
        arrow(0,0,-arrowlengths[1]*cos(thetad_median+pi/2),-arrowlengths[1]*sin(thetad_median+pi/2), color='k',linewidth=1.5)
        
        arrow(0,0,arrowlengths[0]*cos(thetad_all[len(thetad_all)/6]),arrowlengths[0]*sin(thetad_all[len(thetad_all)/6]),color='k',linewidth=.9,linestyle='dashdot')
        arrow(0,0,arrowlengths[0]*cos(thetad_all[5*len(thetad_all)/6]),arrowlengths[0]*sin(thetad_all[5*len(thetad_all)/6]),color='k',linewidth=.9,linestyle='dashdot')
        arrow(0,0,arrowlengths[0]*cos(thetad_all[len(thetad_all)/40]),arrowlengths[0]*sin(thetad_all[len(thetad_all)/40]),color='k',linewidth=.6,linestyle='dotted')
        arrow(0,0,arrowlengths[0]*cos(thetad_all[39*len(thetad_all)/40]),arrowlengths[0]*sin(thetad_all[39*len(thetad_all)/40]),color='k',linewidth=.6,linestyle='dotted')
        arrow(0,0,-arrowlengths[0]*cos(thetad_all[len(thetad_all)/6]),-arrowlengths[0]*sin(thetad_all[len(thetad_all)/6]),linewidth=.9,linestyle='dashdot')
        arrow(0,0,-arrowlengths[0]*cos(thetad_all[5*len(thetad_all)/6]),-arrowlengths[0]*sin(thetad_all[5*len(thetad_all)/6]),linewidth=.9,linestyle='dashdot')
        arrow(0,0,-arrowlengths[0]*cos(thetad_all[len(thetad_all)/40]),-arrowlengths[0]*sin(thetad_all[len(thetad_all)/40]),color='k',linewidth=.6,linestyle='dotted')
        arrow(0,0,-arrowlengths[0]*cos(thetad_all[39*len(thetad_all)/40]),-arrowlengths[0]*sin(thetad_all[39*len(thetad_all)/40]),color='k',linewidth=.6,linestyle='dotted')

        arrow(0,0,arrowlengths[1]*cos(thetad_all[len(thetad_all)/6]+pi/2),arrowlengths[1]*sin(thetad_all[len(thetad_all)/6]+pi/2),color='k',linewidth=.9,linestyle='dashdot')
        arrow(0,0,arrowlengths[1]*cos(thetad_all[5*len(thetad_all)/6]+pi/2),arrowlengths[1]*sin(thetad_all[5*len(thetad_all)/6]+pi/2),color='k',linewidth=.9,linestyle='dashdot')
        arrow(0,0,arrowlengths[1]*cos(thetad_all[len(thetad_all)/40]+pi/2),arrowlengths[1]*sin(thetad_all[len(thetad_all)/40]+pi/2),color='k',linewidth=.6,linestyle='dotted')
        arrow(0,0,arrowlengths[1]*cos(thetad_all[39*len(thetad_all)/40]+pi/2),arrowlengths[1]*sin(thetad_all[39*len(thetad_all)/40]+pi/2),color='k',linewidth=.6, linestyle='dotted')
        arrow(0,0,-arrowlengths[1]*cos(thetad_all[len(thetad_all)/6]+pi/2),-arrowlengths[1]*sin(thetad_all[len(thetad_all)/6]+pi/2),color='k',linewidth=.9,linestyle='dashdot')
        arrow(0,0,-arrowlengths[1]*cos(thetad_all[5*len(thetad_all)/6]+pi/2),-arrowlengths[1]*sin(thetad_all[5*len(thetad_all)/6]+pi/2),color='k',linewidth=.9, linestyle='dashdot')
        arrow(0,0,-arrowlengths[1]*cos(thetad_all[len(thetad_all)/40]+pi/2),-arrowlengths[1]*sin(thetad_all[len(thetad_all)/40]+pi/2),color='k',linewidth=.6,linestyle='dotted')
        arrow(0,0,-arrowlengths[1]*cos(thetad_all[39*len(thetad_all)/40]+pi/2),-arrowlengths[1]*sin(thetad_all[39*len(thetad_all)/40]+pi/2),color='k',linewidth=.6, linestyle='dotted')


        #26. Environment angle                                #
        #27. Environment angle lower bound (1-sigma)        #
        #28. Environment angle upper bound (1-sigma)        #


        #Plot environment angle
        datatable = np.loadtxt('/home/bruclaud/glass/DataTable.txt')
        rows, colums = np.shape(datatable)
        for j in range(rows):
            if datatable[j][0]==galaxynum:
                galaxyrow = j
                break

        if datatable[galaxyrow][26]!=0: arrow(0,0,arrowlengths[0]*cos(datatable[galaxyrow][26]),arrowlengths[0]*sin(datatable[galaxyrow][26]), color='DeepPink',linewidth=1.5)
        if datatable[galaxyrow][27]!=0: arrow(0,0,arrowlengths[0]*cos(datatable[galaxyrow][27]),arrowlengths[0]*sin(datatable[galaxyrow][27]), color='DeepPink',linewidth=.9,linestyle='dashdot')
        if datatable[galaxyrow][28]!=0: arrow(0,0,arrowlengths[0]*cos(datatable[galaxyrow][28]),arrowlengths[0]*sin(datatable[galaxyrow][28]), color='DeepPink',linewidth=.9,linestyle='dashdot')

        end_plot()


    if 1: #bruclaud2012
        begin_plot()
        L = obj.basis.pixrad
        R = obj.basis.mapextent
        refinement = 1
        if galaxynum != 957: a = stellar.copy()
        elif galaxynum == 957 and 1: a = stellarcopy.copy()
        else: a = stellar.copy()

        bins = (2*L+1)
        X = obj.basis.ploc.real
        Y = -obj.basis.ploc.imag
        gridC = histogram2d(Y, X, bins=bins, weights=a*(obj.basis.int_cell_size==1), range=[[-R,R], [-R,R]])[0]
        gridC *= obj.basis.top_level_cell_size**2

        bins = (2*L+1) * refinement
        gridR = histogram2d(Y, X, bins=bins, weights=a*(obj.basis.int_cell_size!=1)*obj.basis.cell_size**2, range=[[-R,R], [-R,R]])[0]
        grid = gridC + gridR
        grid /= obj.basis.top_level_cell_size**2
        grid = log10(grid.copy())#+1e-4)


        kw = default_kw(R)
        #kw.pop('cmap')
        clevels = 20
        pl.over(pl.contour, grid, clevels, extend='both', colors='c', alpha=.9, **kw)
        pl.gca().set_aspect('equal')
        pl.ylim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
        pl.xlim([-obj.basis.cell_size[-1]*(obj.basis.pixrad+.5),obj.basis.cell_size[-1]*(obj.basis.pixrad+.5)]) #############################################
        pl.xlabel(r'$-\Delta\alpha \ \left[\mathrm{arcsec}\right]$')
        pl.ylabel(r'$\Delta\delta \ \left[\mathrm{arcsec}\right]$')

        arrow(0,0,V1s/V2s*cos(thetas)*resizefactors,V1s/V2s*sin(thetas)*resizefactors, color='k',linewidth=1.5)
        arrow(0,0,cos(thetas+pi/2)*resizefactors,sin(thetas+pi/2)*resizefactors, color='k',linewidth=1.5)
        arrow(0,0,-V1s/V2s*cos(thetas)*resizefactors,-V1s/V2s*sin(thetas)*resizefactors, color='k',linewidth=1.5)
        arrow(0,0,-cos(thetas+pi/2)*resizefactors,-sin(thetas+pi/2)*resizefactors, color='k',linewidth=1.5)
        
        end_plot()


    if 1: #bruclaud2012
        begin_plot()
        pl.hist(thetad_all, 50, histtype='step')
        pl.xlabel(r'$\theta_{dm} \ \left[\mathrm{radian}\right]$')
        pl.ylabel(r'$\mathrm{Counts}$')
        pl.xlim(xmax=pl.xlim()[1] + 0.01*(pl.xlim()[1] - pl.xlim()[0]))
        pl.ylim(ymax=pl.ylim()[1] + 0.01*(pl.ylim()[1] - pl.ylim()[0]))
        end_plot()


    if 1: #bruclaud2012
        begin_plot()
        pl.hist(eigvalueratiod_all, 50, histtype='step')
        pl.xlabel(r'$\lambda_{1}/\lambda_{2}$')
        pl.ylabel(r'$\mathrm{Counts}$')
        pl.xlim(xmax=pl.xlim()[1] + 0.01*(pl.xlim()[1] - pl.xlim()[0]))
        pl.ylim(ymax=pl.ylim()[1] + 0.01*(pl.ylim()[1] - pl.ylim()[0]))
        end_plot()


    if 1: #bruclaud2012
        #Initialize plotting (need to add something too if we want only subfiles produced!)
        if not produce_subfiles:
            axes1 = gcf().add_subplot(fig_nr,fig_nc,fig_subplot_index)
            fig_subplot_index += 1
        else:
            f = figure(figsize=(fig_plot_size*fig_nc, fig_plot_size*fig_nr))
            axes1 = f.add_subplot(fig_nr,fig_nc,1)
            f.subplots_adjust(left=leftwidth, right=rightwidth)
            fig_subplot_index += 1


        #Plotting the average data points at different radii
        #Calculate stellar kappa(R)
        kappaRs = zeros(pixelradius+1) #pixrad
        if galaxynum != 957:
            for k in range(pixelradius+1): #pixrad
                for l in obj.basis.rings[k]:
                    kappaRs[k] += stellar[l]
                kappaRs[k] /= obj.basis.rings[k].size
        else:
            for k in range(pixelradius+1): #pixrad
                counter = 0
                for l in obj.basis.rings[k]:
                    kappaRs[k] += stellarcopy[l]
                    if stellarcopy[l] != 0: counter += 1
                if counter != 0: kappaRs[k] /= counter #Divide by number of pixels with information
                else: kappaRs[k] = 0
                print k,': Counter =',counter,' and  Number =',obj.basis.rings[k].size


        #Now we calculate for each data point the dark matter kappa and take the median
        kappaRd_median = zeros(pixelradius+1) #pixrad
        kappaRd_1sigmaplus = zeros(pixelradius+1) #pixrad
        kappaRd_1sigmaminus = zeros(pixelradius+1) #pixrad
        kappaRd_maxdevplus = zeros(pixelradius+1) #pixrad
        kappaRd_maxdevminus = zeros(pixelradius+1) #pixrad

        for k in range(pixelradius+1): #pixrad
            kappaRd_k_all = zeros(0)
            for m in g.models:
                obj,ps = m['obj,data'][0]
                kappaRd_model = ps['kappa(R)'][k]-kappaRs[k]
                kappaRd_k_all = np.append(kappaRd_k_all,kappaRd_model)
            kappaRd_k_all = np.sort(kappaRd_k_all)
            kappaRd_median[k] = kappaRd_k_all[len(kappaRd_k_all)/2]
            kappaRd_1sigmaplus[k] = kappaRd_k_all[5*len(kappaRd_k_all)/6]
            kappaRd_1sigmaminus[k] = kappaRd_k_all[len(kappaRd_k_all)/6]
            kappaRd_maxdevplus[k] = kappaRd_k_all[-1]
            kappaRd_maxdevminus[k] = kappaRd_k_all[0]

        #Plot
        pl.yscale('log')
        pl.xscale('linear')

        if 0: #Plot twin-scale
            errorbar(data['R']['arcsec'],kappaRs+kappaRd_median,yerr=[kappaRd_median-kappaRd_1sigmaminus,kappaRd_1sigmaplus-kappaRd_median],marker='.',linestyle='-',color='k',linewidth=1.8)
            errorbar(data['R']['arcsec'],kappaRd_median,yerr=[kappaRd_median-kappaRd_maxdevminus,kappaRd_maxdevplus-kappaRd_median],markerfacecolor='g',ecolor='k',color='g',linewidth=1.)
            errorbar(data['R']['arcsec'],kappaRd_median,yerr=[kappaRd_median-kappaRd_1sigmaminus,kappaRd_1sigmaplus-kappaRd_median],marker='.',linestyle='-',color='g',linewidth=1.8)
            plot(data['R']['arcsec'],kappaRs,marker='.',linestyle='-',color='c',linewidth=1.8)
            pl.ylabel(r'$\left<\kappa(R)\right> \ \left[\Sigma_{cr}\right]$')

            #Plot the vertical lines
            for i,src in enumerate(obj.sources):
                for img in src.images:
                    temporaryradius = sqrt(img.pos.real**2+img.pos.imag**2)
                    if temporaryradius == maxradius: pl.axvline(x=temporaryradius,linewidth=1.5,color='r')
                    else: pl.axvline(x=temporaryradius,linewidth=.5,color='r')

            #Set the ticks in arsec and plot the scale
            ticks_array_arcsec = get_xticks_arcsec(data['R']['arcsec'][-1],galaxynum)
            xticks(ticks_array_arcsec)
            pl.xlabel(r'$R \ \left[\mathrm{arcsec}\right]$')

            #Set the ticks in the twin-scale above the plot in kpc and plot the scale
            axes2 = axes1.twiny()
            ticks_array_kpc, ticks_label_kpc = get_xticks_kpc(data['R']['kpc'][-1],ticks_array_arcsec[-1],galaxynum,obj.dL,data['nu'])
#            plot(data['R']['arcsec'],kappaRs+kappaRd_median,marker='.',linestyle='-',color='k',linewidth=1.8)
#            plot(data['R']['arcsec'],kappaRs,marker='.',linestyle='-',color='c',linewidth=1.8)
#            plot(data['R']['arcsec'],kappaRd_median,color='g',linewidth=1.8)
            xticks(ticks_array_kpc,ticks_label_kpc)
            pl.xlabel(r'$R \ \left[\mathrm{kpc}\right]$')

        if 1: #Plot physical scales
            errorbar(data['R']['kpc'],kappaRs+kappaRd_median,yerr=[kappaRd_median-kappaRd_1sigmaminus,kappaRd_1sigmaplus-kappaRd_median],marker='.',linestyle='-',color='k',linewidth=1.8)
            errorbar(data['R']['kpc'],kappaRd_median,yerr=[kappaRd_median-kappaRd_maxdevminus,kappaRd_maxdevplus-kappaRd_median],markerfacecolor='g',ecolor='k',color='g',linewidth=1.)
            errorbar(data['R']['kpc'],kappaRd_median,yerr=[kappaRd_median-kappaRd_1sigmaminus,kappaRd_1sigmaplus-kappaRd_median],marker='.',linestyle='-',color='g',linewidth=1.8)
            plot(data['R']['kpc'],kappaRs,marker='.',linestyle='-',color='c',linewidth=1.8)
            pl.ylabel(r'$\left<\kappa(R)\right> \ \left[\Sigma_{cr}\right]$')

            #Plot the vertical lines
            for i,src in enumerate(obj.sources):
                for img in src.images:
                    temporaryradius = sqrt(img.pos.real**2+img.pos.imag**2)
                    temporaryradius_kpc = convert('arcsec to kpc',temporaryradius, obj.dL, data['nu'])
                    if temporaryradius == maxradius: pl.axvline(x=temporaryradius_kpc,linewidth=1.5,color='r')
                    else: pl.axvline(x=temporaryradius_kpc,linewidth=.5,color='r')

            pl.xlabel(r'$R \ \left[\mathrm{kpc}\right]$')

        end_plot() #maybe remove

    if 1: #bruclaud2012
        #Initialize plotting (need to add something too if we want only subfiles produced!)
        if not produce_subfiles:
            axes1 = gcf().add_subplot(fig_nr,fig_nc,fig_subplot_index)
            fig_subplot_index += 1
        else:
            f = figure(figsize=(fig_plot_size*fig_nc, fig_plot_size*fig_nr))
            axes1 = f.add_subplot(fig_nr,fig_nc,1)
            f.subplots_adjust(left=leftwidth, right=rightwidth)
            fig_subplot_index += 1


        #Plotting the average data points at different radii
        #Calculate stellar kappa(R)
        massRs = zeros(pixelradius+1) #pixrad
        if galaxynum != 957:
            for k in range(pixelradius+1): #pixrad
                for l in obj.basis.rings[k]:
                    massRs[k] += (obj.basis.cell_size[l])**2*(stellar[l]*dscale) #############################################
                if k>0:
                    massRs[k] += massRs[k-1]
        else:
            for k in range(pixelradius+1): #pixrad
                counter = 0
                for l in obj.basis.rings[k]:
                    if stellarcopy[l] != 0: counter += 1
                    massRs[k] += (obj.basis.cell_size[l])**2*(stellarcopy[l]*dscale) #############################################
                if counter != 0: ratio = float(obj.basis.rings[k].size)/float(counter)
                else: ratio = 0
                massRs[k] *= ratio
                print k,': Counter =',counter,' and  Number =',obj.basis.rings[k].size,' and  Ratio =',ratio
                if k>0:
                    massRs[k] += massRs[k-1]


        #Now we calculate for each data point the dark matter kappa and take the median
        massRd_median = zeros(pixelradius+1) #pixrad
        massRd_1sigmaplus = zeros(pixelradius+1) #pixrad
        massRd_1sigmaminus = zeros(pixelradius+1) #pixrad
        massRd_2sigmaplus = zeros(pixelradius+1) #pixrad
        massRd_2sigmaminus = zeros(pixelradius+1) #pixrad
        massRd_maxdevplus = zeros(pixelradius+1) #pixrad
        massRd_maxdevminus = zeros(pixelradius+1) #pixrad

        for k in range(pixelradius+1): #pixrad
            massRd_k_all = zeros(0)
            for m in g.models:
                obj,ps = m['obj,data'][0]
                massRd_model = ps['M(<R)'][k]-massRs[k]
                massRd_k_all = np.append(massRd_k_all,massRd_model)
            massRd_k_all = np.sort(massRd_k_all)
            massRd_median[k] = massRd_k_all[len(massRd_k_all)/2]
            massRd_1sigmaplus[k] = massRd_k_all[5*len(massRd_k_all)/6]
            massRd_1sigmaminus[k] = massRd_k_all[len(massRd_k_all)/6]
            massRd_2sigmaplus[k] = massRd_k_all[39*len(massRd_k_all)/40]
            massRd_2sigmaminus[k] = massRd_k_all[len(massRd_k_all)/40]
            massRd_maxdevplus[k] = massRd_k_all[-1]
            massRd_maxdevminus[k] = massRd_k_all[0]

        #Errorbars for the total mass
        massR_median = massRd_median+massRs
        massR_1sigmaplus = massRs+massRd_1sigmaplus
        massR_1sigmaminus = massRs+massRd_1sigmaminus
        massR_2sigmaplus = massRs+massRd_2sigmaplus
        massR_2sigmaminus = massRs+massRd_2sigmaminus

        #Plot
        pl.yscale('log')
        pl.xscale('linear')

        if 0: #Plot twin scale
            errorbar(data['R']['arcsec'],massR_median,yerr=[massRd_median-massRd_1sigmaminus,massRd_1sigmaplus-massRd_median],marker='.',linestyle='-',color='k',linewidth=1.8)
            errorbar(data['R']['arcsec'],massRd_median,yerr=[massRd_median-massRd_maxdevminus,massRd_maxdevplus-massRd_median],markerfacecolor='g',ecolor='k',color='g',linewidth=1.)
            errorbar(data['R']['arcsec'],massRd_median,yerr=[massRd_median-massRd_1sigmaminus,massRd_1sigmaplus-massRd_median],marker='.',linestyle='-',color='g',linewidth=1.8)
            plot(data['R']['arcsec'],massRs,marker='.',linestyle='-',color='c',linewidth=1.8)
            pl.ylabel(r'$\mathrm{M(<R)} \ \left[M_{\odot}\right]$')

            #Plot the vertical lines
            for i,src in enumerate(obj.sources):
                for img in src.images:
                    temporaryradius = sqrt(img.pos.real**2+img.pos.imag**2)
                    if temporaryradius == maxradius: pl.axvline(x=temporaryradius,linewidth=1.5,color='r')
                    else: pl.axvline(x=temporaryradius,linewidth=.5,color='r')

            #Set the ticks in arsec and plot the scale
            ticks_array_arcsec = get_xticks_arcsec(data['R']['arcsec'][-1],galaxynum)
            xticks(ticks_array_arcsec)
            pl.xlabel(r'$R \ \left[\mathrm{arcsec}\right]$')

            #Set the ticks in the twin-scale above the plot in kpc and plot the scale
            axes2 = axes1.twiny()
            ticks_array_kpc, ticks_label_kpc = get_xticks_kpc(data['R']['kpc'][-1],ticks_array_arcsec[-1],galaxynum,obj.dL,data['nu'])
#            plot(data['R']['arcsec'],massR_median,marker='.',linestyle='-',color='k',linewidth=1.8)
#            plot(data['R']['arcsec'],massRs,marker='.',linestyle='-',color='c',linewidth=1.8)
#            plot(data['R']['arcsec'],massRd_median,marker='.',linestyle='-',color='g',linewidth=1.8)
            xticks(ticks_array_kpc,ticks_label_kpc)
            pl.xlabel(r'$R \ \left[\mathrm{kpc}\right]$')

        if 1: #Plot physical scales
            errorbar(data['R']['kpc'],massR_median,yerr=[massRd_median-massRd_1sigmaminus,massRd_1sigmaplus-massRd_median],marker='.',linestyle='-',color='k',linewidth=1.8)
            errorbar(data['R']['kpc'],massRd_median,yerr=[massRd_median-massRd_maxdevminus,massRd_maxdevplus-massRd_median],markerfacecolor='g',ecolor='k',color='g',linewidth=1.)
            errorbar(data['R']['kpc'],massRd_median,yerr=[massRd_median-massRd_1sigmaminus,massRd_1sigmaplus-massRd_median],marker='.',linestyle='-',color='g',linewidth=1.8)
            plot(data['R']['kpc'],massRs,marker='.',linestyle='-',color='c',linewidth=1.8)
            pl.ylabel(r'$\mathrm{M(<R)} \ \left[M_{\odot}\right]$')

            #Plot the vertical lines
            for i,src in enumerate(obj.sources):
                for img in src.images:
                    temporaryradius = sqrt(img.pos.real**2+img.pos.imag**2)
                    temporaryradius_kpc = convert('arcsec to kpc',temporaryradius, obj.dL, data['nu'])
                    if temporaryradius == maxradius: pl.axvline(x=temporaryradius_kpc,linewidth=1.5,color='r')
                    else: pl.axvline(x=temporaryradius_kpc,linewidth=.5,color='r')

            pl.xlabel(r'$R \ \left[\mathrm{kpc}\right]$')

        end_plot() #maybe remove

        
    if 0:
        for g in gls:
            begin_plot()
            g.glhist('N1', label='N1', color='r', xlabel=r'$\theta_E$')
            #g.glhist('N3', label='N3', color='b', xlabel=r'$\theta_E$')
            #g.glhist('N4', label='N4', color='m', xlabel=r'$\theta_E$')
            g.glhist('N2', label='N2', color='g', xlabel=r'$\theta_E$')
            #g.glhist('N5', label='N5', color='c', xlabel=r'$\theta_E$')

    print '4/7' #bruclaud2012


    if 1:
        for g in gls:
            begin_plot()
            g.shear_plot()
            pl.ylabel('$\mathrm{Counts}$')
            end_plot()

    print '5/7' #bruclaud2012


    if 1:
        for g in gls:
            begin_plot()
            g.time_delays_plot()
            pl.ylabel('$\mathrm{Counts}$')
            end_plot()


    print '6/7' #bruclaud2012


    if 0 and (galaxynum == 47 or galaxynum == 1115 or galaxynum == 1422): #bruclaud2012
        #Initialize plotting (need to add something too if we want only subfiles produced!)
        axes2 = gcf().add_subplot(fig_nr,fig_nc,fig_subplot_index)
        fig_subplot_index += 1

        #Create filename
        fname1 = '/home/bruclaud/glass/Samples/'+str(galaxynumstring)+'_env1.png'

        img1 = pl.imread(fname1)

        pl.imshow(img1)
        axes2.set_frame_on(False)
        axes2.axes.get_yaxis().set_visible(False)
        axes2.axes.get_xaxis().set_visible(False)
        end_plot()


    if 0 and (galaxynum == 47 or galaxynum == 1115 or galaxynum == 1422): #bruclaud2012
        #Initialize plotting (need to add something too if we want only subfiles produced!)
        axes3 = gcf().add_subplot(fig_nr,fig_nc,fig_subplot_index)
        fig_subplot_index += 1

        #Create filename
        fname2 = '/home/bruclaud/glass/Samples/'+str(galaxynumstring)+'_env2.png'

        img2 = pl.imread(fname2)

        pl.imshow(img2)
        axes3.set_frame_on(False)
        axes3.axes.get_yaxis().set_visible(False)
        axes3.axes.get_xaxis().set_visible(False)
        end_plot()


    if 1:
        for g in gls:
            begin_plot()
            pmvector = zeros(0)
            for u in g.models:
                obj,ps = u['obj,data'][0]
                pmvector = np.append(pmvector,ps['PM'])

            pmvector = np.sort(pmvector)
            pl.hist(pmvector,20,histtype='step',color='g')
            pl.xlabel(r'$\mathrm{Point \ mass} \ \left[\theta_{E}\right]$')
            pl.ylabel('Counts')


    if 1 and datatable_still_to_fill: #bruclaud2012
        #################################################
        #Contents of explanationtable.txt                #
        #0. Galaxy ID                                        #
        #1. Problematic (1 = Yes)                        #
        #2. Double (1 = Yes, 0 = Quad, 2 = Special Quad)#

        #3. Theta dm                                        #
        #4. Theta dm lower bound (1-sigma)                #
        #5. Theta dm upper bound (1-sigma)                #
        #6. Theta dm lower bound (2-sigma)                #
        #7. Theta dm upper bound (2-sigma)                #
        #8. Theta stellar                                #

        #9. Eigenvalue ratio dm                                #
        #10. Eigenvalue ratio dm lower bound (1-sigma)        #
        #11. Eigenvalue ratio dm upper bound (1-sigma)        #
        #12. Eigenvalue ratio dm lower bound (2-sigma)        #
        #13. Eigenvalue ratio dm upper bound (2-sigma)        #
        #14. Eigenvalue ratio stellar                        #

        #15. Included mass                                #
        #16. Included dm                                #
        #17. Included dm lower bound (1-sigma)                #
        #18. Included dm upper bound (1-sigma)                #
        #19. Included dm lower bound (2-sigma)                #
        #20. Included dm upper bound (2-sigma)                #

        #21. Included mass ratio                        #
        #22. Included mass ratio lower bound (1-sigma)        #
        #23. Included mass ratio upper bound (1-sigma)        #
        #24. Included mass ratio lower bound (2-sigma)        #
        #25. Included mass ratio upper bound (2-sigma)        #

        #26. Environment angle                                #
        #27. Environment angle lower bound (1-sigma)        #
        #28. Environment angle upper bound (1-sigma)        #
        #29. Distance to centroid                        #
        #30. Distance to centroid lower bound (1-sigma)        #
        #31. Distance to centroid upper bound (1-sigma)        #
        #32. Number of objects in environment                #

        #33. Date when last modified                        #
        #################################################


        #Here we fill the DataTable.txt-file
        for j in range(rows):
            if datatable[j][0] == galaxynum:
                mod_row = j
                break

        #Find data-point data['R'] which still lies in the maxradius-circle of the last image
        max_index = 0
        for j in range(len(data['R']['arcsec'])):
            if data['R']['arcsec'][j] > maxradius: break
            max_index = j

        #massR_1sigmaminus = (massRd_median - massRd_1sigmaminus)*sqrt(1+(massRd_median/massR_median)**2)/massR_median + massR_median
        #massR_1sigmaplus = (massRd_1sigmaplus-massRd_median)*sqrt(1+(massRd_median/massR_median)**2)/massR_median + massR_median
        #massR_2sigmaminus = 
        #massR_2sigmaplus = 

        datatable[mod_row][3] = thetad_median
        datatable[mod_row][4] = thetad_all[len(thetad_all)/6]
        datatable[mod_row][5] = thetad_all[5*len(thetad_all)/6]
        datatable[mod_row][6] = thetad_all[len(thetad_all)/40]
        datatable[mod_row][7] = thetad_all[39*len(thetad_all)/40]
        datatable[mod_row][8] = thetas

        datatable[mod_row][9] = eigvalueratiod_median
        datatable[mod_row][10] = eigvalueratiod_all[len(eigvalueratiod_all)/6]
        datatable[mod_row][11] = eigvalueratiod_all[5*len(eigvalueratiod_all)/6]
        datatable[mod_row][12] = eigvalueratiod_all[len(eigvalueratiod_all)/40]
        datatable[mod_row][13] = eigvalueratiod_all[39*len(eigvalueratiod_all)/40]
        datatable[mod_row][14] = V1s/V2s

        datatable[mod_row][15] = massR_median[max_index]
        datatable[mod_row][16] = massRd_median[max_index]
        datatable[mod_row][17] = massRd_1sigmaminus[max_index]
        datatable[mod_row][18] = massRd_1sigmaplus[max_index]
        datatable[mod_row][19] = massRd_2sigmaminus[max_index]
        datatable[mod_row][20] = massRd_2sigmaplus[max_index]

        datatable[mod_row][21] = massRd_median[max_index]/massR_median[max_index]
        datatable[mod_row][22] = massRd_median[max_index]/massR_median[max_index]-(massRd_median[max_index]-massRd_1sigmaminus[max_index])*massRs[max_index]/(massR_median[max_index])**2
        datatable[mod_row][23] = massRd_median[max_index]/massR_median[max_index]+(massRd_1sigmaplus[max_index]-massRd_median[max_index])*massRs[max_index]/(massR_median[max_index])**2
        datatable[mod_row][24] = massRd_median[max_index]/massR_median[max_index]-(massRd_median[max_index]-massRd_2sigmaminus[max_index])*massRs[max_index]/(massR_median[max_index])**2
        datatable[mod_row][25] = massRd_median[max_index]/massR_median[max_index]+(massRd_2sigmaplus[max_index]-massRd_median[max_index])*massRs[max_index]/(massR_median[max_index])**2

        datatable[mod_row][33] = datetime.date.today().year*10000+datetime.date.today().month*100+datetime.date.today().day

        np.savetxt('/home/bruclaud/glass/DataTable2.txt',datatable)


    print '7/7' #bruclaud2012


#-------------------------------------------------------------------------------

ion()
opts = Environment.global_opts['argv']
gls = [loadstate(f) for f in opts[1:]]

if len(gls) == 1:
    colors = 'k'
else:
    colors = 'rgbcm'

datatable_still_to_fill = True

PlotFigures()

if produce_both_subfiles_and_one_plot:
    datatable_still_to_fill = False
    produce_subfiles = False
    fig_subplot_index= 1
    PlotFigures()
    savefig('%s.eps' % subfilespath)

ioff()
if show_plots: show()

