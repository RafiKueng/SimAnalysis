from numpy import linspace, zeros, amin, amax
from pylab import contour, figure, savefig, show
from Laplace_function import Laplace
from kappas import kappa_SIE, poten_shear, kappa_NFW

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


    
def SIE(gal,x,y):
    z = zeros((len(y),len(x)))
    re,ell,ell_pa = float(gal[1]), float(gal[2]), float(gal[3])
    print 'Einstein radius',re
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = kappa_SIE(x[i],y[j],re,ell,ell_pa)
    print 'max kappa',amax(z)
    return z

def NFW(gal,x,y):
    z = zeros((len(y),len(x)))
    gx,gy = float(gal[1]), float(gal[2])
    kap,rsc = float(gal[3]), float(gal[4])
    ell,pa = float(gal[5]),float(gal[6])
    print 'pos',gx,gy
    print 'kap,rsc',kap,rsc
    print 'ell,pa',ell,pa
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = kappa_NFW(x[i],y[j],gx,gy,kap,rsc,ell,pa)
    print 'max kappa',amax(z)
    return z

def grids(asw,x,y):
    obj = sim[asw]
    src = obj[1]
    arriv = geom(src,x,y)
    if obj[0]=='quasar' or obj[0]=='galaxy':
        gal = obj[2]
        kappa = SIE(gal,x,y)            
        arriv -= shear(obj[3],x,y)
        delta = x[1]-x[0]
        arriv += Laplace(2*kappa*delta**2)
    if obj[0]=='cluster':
        kappa = 0*arriv
        clus = obj[2]
        for gal in clus:
            kappa += NFW(gal,x,y)
        delta = x[1]-x[0]
        arriv += Laplace(2*kappa*delta**2)
    return (kappa, arriv)
    


def draw(asw):
    print asw
    if sim[asw][0] == 'cluster':
        R,N,M = 100,50,25
    else:
        R,N,M = 50,50,1
    x = linspace(-R,R,2*N)
    y = 1*x
    kappa, arriv = grids(asw,x,y)
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lev = linspace(0,amax(kappa),20)
    pc = panel.contour(x,y,kappa,lev)
    panel.clabel(pc, inline=1, fontsize=10)
    savefig(asw+'_kappa.png')
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    x = x[M:-M]
    y = y[M:-M]
    arriv = arriv[M:-M,M:-M]
    lo,hi = amin(arriv), amax(arriv)
    lev = linspace(lo,lo+0.05*(hi-lo),50)
    panel.contour(x,y,arriv,lev)
    savefig(asw+'_arriv.png')
    show()
    
for asw in sim:
    if sim[asw][0] == 'cluster':
        draw(asw)
        break



