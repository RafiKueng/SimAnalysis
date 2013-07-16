from numpy import pi, cos, sin, arctan2, linspace, zeros, amin, amax
from pylab import contour, figure, show

import params
sim = params.read()

# for asw in sim:
#    print asw, sim[asw]

def geom(asw,x,y,z):
    g = 1*z
    src = sim[asw][1]
    bx,by = float(src[1]), float(src[2])
    for i in range(len(x)):
        for j in range(len(y)):
            g[j,i] = ((x[i]-bx)**2 + (y[j]-by)**2)/2
    return g

def shear(asw,x,y,z):
    s = 1*z
    xs = sim[asw][3]
    print xs
    gam,th = float(xs[1]), float(xs[2])*pi/180
    gam1, gam2 = gam*cos(2*th), gam*sin(2*th)
    for i in range(len(x)):
        for j in range(len(y)):
            s[j,i] = (x[i]**2 - y[j]**2)*gam1/2 + x[i]*y[i]*gam2
    return s


def kappa(asw,x,y,z):
    k = 1*z
    gal = sim[asw][2]
    print gal
    re,ell,pa = float(gal[1]), float(gal[2]), float(gal[3])*pi/180
    for i in range(len(x)):
        for j in range(len(y)):
            phi = arctan2(y[j],x[i]) - pa
            th2r = x[i]**2 + y[j]**2 + 1e-6
            th2p = 1 - ell*cos(2*phi)
            theta = (th2r*th2p)**.5
            k[j,i] = re/theta
    return k

N = 200
R = 5
x = linspace(-R,R,N)
y = 1*x
z = zeros((N,N))

fig = figure()
panel = fig.add_subplot(1,1,1)
panel.set_aspect('equal')

#f = geom('ASW0002b6m',x,y,z)
#f = shear('ASW0002b6m',x,y,z)
f = kappa('ASW0002b6m',x,y,z)
lev = linspace(amin(f),amax(f),100)
panel.contour(x,y,f,lev)

show()
