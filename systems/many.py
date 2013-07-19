from numpy import linspace, zeros, amin, amax, sqrt, pi
from pylab import contour, figure, savefig, show
from poten import poten_SIE, poten_NFW, poten_shear
from angdiam import dratio

from matplotlib import rc
rc('text', usetex=True)
# rc('font', family='serif')

import params
sim = params.read()

def geom(src,x,y):
    z = zeros((len(y),len(x)))
    bx,by = float(src[1]), float(src[2])
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = ((x[i]-bx)**2 + (y[j]-by)**2)/2
    return z


def shear(xs,x,y):  
    z = zeros((len(y),len(x)))
    sh,pa = float(xs[1]), float(xs[2])
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = poten_shear(x[i],y[j],sh,pa)
    return z


def poten_gal(gal,x,y):
    z = zeros((len(y),len(x)))
    re,ell,ell_pa = float(gal[1]), float(gal[2]), float(gal[3])
    print 'Einstein radius',re
    print 'ellipticity',ell
    print 'pos ang',ell_pa
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = poten_SIE(x[i],y[j],re,ell,ell_pa)
    return z

def poten_clus(clus,zsrc,x,y):
    z = zeros((len(y),len(x)))
    kaps = float(clus[0][1])
    rsc = float(clus[0][2])
    zlens = float(clus[1][3])
    fudge = dratio(zlens,zsrc)
    print 'kaps,rsc',kaps,rsc
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = fudge * poten_NFW(x[i],y[j],kaps,rsc)
    for g in range(1,len(clus)):
        gal = clus[g]
        gx,gy = float(gal[1]), float(gal[2])
        zlens = float(gal[3])
        fudge = dratio(zlens,zsrc)
        sig = float(gal[4])
        print 'sigma', sig
        ell,pa = float(gal[5]),float(gal[6])
        reinst = 4*pi*(sig/3e5)**2 * 206265/.185 * fudge
        print 'pos',gx,gy
        print 'reinst,ell,pa',reinst,ell,pa
        for i in range(len(x)):
            for j in range(len(y)):
                z[j,i] += poten_SIE(x[i]-gx,y[j]-gy,reinst,ell,pa)
    return z

def grids(asw,x,y):
    obj = sim[asw]
    basic = geom(obj[1],x,y)
    if obj[0]=='quasar' or obj[0]=='galaxy':
        gal = obj[2]
        poten = poten_gal(gal,x,y)            
        basic -= shear(obj[3],x,y)
    else:
        zsrc = float(obj[1][-1])
        clus = obj[2]
        poten = poten_clus(clus,zsrc,x,y) 
    kappa = 0*poten
    kappa[1:-1,1:-1] = poten[0:-2,1:-1] + poten[2:,1:-1] \
                     + poten[1:-1,0:-2] + poten[1:-1,2:] \
                     - 4*poten[1:-1,1:-1]
    dx = x[1]-x[0]
    kappa /= 2*dx*dx
    return (kappa,basic-poten)

def draw(asw):
    print asw
    N,R = 100,50
    if sim[asw][0] == 'quasar':
        flag,R = 'Q',20
    if sim[asw][0] == 'galaxy':
        flag,R = 'G',20
    if sim[asw][0] == 'cluster':
        flag,R = 'C',50
    x = linspace(-R,R,N)
    y = 1*x
    kappa,arriv = grids(asw,x,y)
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lev = linspace(0,10,41)
    pc = panel.contour(x,y,kappa,lev)
    panel.clabel(pc, inline=1, fontsize=10)
    savefig('figs/'+asw+flag+'_kappa.png')
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    rad = linspace(0,R,20)[1:]
    radq = rad*rad
    sum = 0*rad
    for i in range(len(x)):
        for j in range(len(y)):
            rsq = x[i]**2 + y[j]**2
            for k in range(len(rad)):
                if rsq < radq[k]:
                    sum[k] += kappa[j,i]
    dx = x[1]-x[0]
    for k in range(len(rad)):
        sum[k] *= dx*dx/(pi*radq[k])
    panel.scatter(rad,sum)
    panel.set_xlabel('radius in pixels')
    panel.set_ylabel('average interior $\kappa$')
    savefig('figs/'+asw+flag+'_menc.png')
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lo,hi = amin(arriv), amax(arriv)
    lev = linspace(lo,lo+.2*(hi-lo),100)
    panel.contour(x,y,arriv,lev)
    savefig('figs/'+asw+flag+'_arriv.png')
    show()

for asw in sim:
    draw(asw)


