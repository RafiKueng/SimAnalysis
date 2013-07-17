from numpy import pi, cos, sin, arctan2, linspace, zeros, amin, amax
from pylab import contour, figure, savefig, show
from Laplace_function import Laplace

import params
sim = params.read()


def geom(src,x,y):
    z = zeros((len(x),len(y)))
    bx,by = float(src[1]), float(src[2])
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = ((x[i]-bx)**2 + (y[j]-by)**2)/2
    return z


def shear(xs,X,Y):  
    z = zeros((len(Y),len(X)))
    gam,thg = float(xs[1]), float(xs[2])*pi/180 + pi/2
    for i in range(len(X)):
        for j in range(len(Y)):
            x,y = X[i],Y[j]
            rsq = x*x + y*y
            f = 2*(arctan2(y,x) - thg)
            z[j,i] = -gam/2*rsq*cos(f)
    return z


    
def SIE(gal,x,y):
    z = zeros((len(x),len(y)))
    re,ell = float(gal[1]), float(gal[2])
    pa = float(gal[3])*pi/180 + pi/2
    print 'Einstein radius',re
    for i in range(len(x)):
        for j in range(len(y)):
            phi = arctan2(y[j],x[i]) - pa
            th2r = x[i]**2 + y[j]**2 + 1e-6
            th2p = 1 - ell*cos(2*phi)
            theta = (th2r*th2p)**.5
            z[j,i] = re/theta
    return z    

def grids(asw,x,y):
    obj = sim[asw]
    src = obj[1]
    arriv = geom(src,x,y)
    arriv -= shear(obj[3],x,y)
    if obj[0]=='quasar' or obj[0]=='galaxy':
        gal = obj[2]
        kappa = SIE(gal,x,y)            
        delta = x[1]-x[0]
        arriv += Laplace(2*kappa*delta**2)
    return (kappa, arriv)
    


def draw(asw):
    print asw
    N = 100
    R = 50
    x = linspace(-R,R,N)
    y = 1*x
    kappa, arriv = grids(asw,x,y)
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lev = linspace(0,amax(kappa),30)
    panel.contour(x,y,kappa,lev)
    savefig(asw+'_kappa.png')
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    lo,hi = amin(arriv), amax(arriv)
    lev = linspace(lo,lo+0.05*(hi-lo),30)
    panel.contour(x,y,arriv,lev)
    savefig(asw+'_arriv.png')
    
for asw in sim:
    if sim[asw][0] != 'cluster':
        draw(asw)


#kappa, arriv = grids('ASW0002b6m',x,y)
#kappa, arriv = grids('ASW000102p',x,y)
#kappa, arriv = grids('ASW00019rw',x,y)
#kappa, arriv = grids('ASW0000r8n',x,y)
#kappa, arriv = grids('ASW0001hpf',x,y)
#kappa, arriv = grids('ASW0000h2m',x,y)

