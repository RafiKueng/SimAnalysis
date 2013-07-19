from numpy import linspace, zeros, amin, amax, sqrt
from pylab import contour, figure, savefig, show
from poisson import Laplace
from kappas import kappa_SIE, poten_shear, kappa_NFW

import params
sim = params.read()
print len(sim),'sims'

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
    


def draw(asw,R=50):
    print asw
    N = 100
    x = linspace(-R,R,N)
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
    lo,hi = amin(arriv), amax(arriv)
    lev = linspace(lo,lo+.2*(hi-lo),100)
    panel.contour(x,y,arriv,lev)
    savefig(asw+'_arriv.png')
    
def all():
    draw('ASW00004k0')
    draw('ASW0000ar2')
    draw('ASW0000bl0',300)
    draw('ASW0000bsh',400)
    draw('ASW0000e28')
    draw('ASW0000h2m')
    draw('ASW0000kad',100)
    draw('ASW0000r8n')
    draw('ASW0000vqg',120)
    draw('ASW0000w54')
    draw('ASW000102p')
    draw('ASW00013ml',200)
    draw('ASW000195x',500)
    draw('ASW00019rw')
    draw('ASW0001a2m')
    draw('ASW0001a8c')
    draw('ASW0001d74',100)
    draw('ASW0001gve')
    draw('ASW0001hpf')
    draw('ASW0001sym',100)
    draw('ASW00023pg')
    draw('ASW0002b6m')
    draw('ASW0002jo0')
    draw('ASW0002z6f',250)
    draw('ASW00031ve',200)
    draw('ASW0003ctp')
    draw('ASW0004nfh',300)
    draw('ASW0004oux')
    draw('ASW00054e9')
    
#draw('ASW0000kad',100)
#draw('ASW0001sym',200)
draw('ASW0002b6m')
show()