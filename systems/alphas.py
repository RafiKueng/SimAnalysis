from numpy import sqrt, pi, cos, sin, arctan2, arctan, arctanh
from numpy import linspace, zeros
from pylab import contour, figure, show

import params
sim = params.read()

for s in sim:
    if sim[s][0] == 'quasar':
        print s,sim[s][0],sim[s][-1]

def geom(src,x,y):
    z = zeros((2,len(y),len(x)))
    bx,by = float(src[1]), float(src[2])
    print 'source pos',bx,by
    for i in range(len(x)):
        for j in range(len(y)):
            z[0,j,i] = x[i] - bx
            z[1,j,i] = y[j] - by
    return z

def shear(xs,X,Y):
    z = zeros((2,len(Y),len(X)))
    gam,thg = float(xs[1]), float(xs[2])*pi/180
    cs,sn = cos(2*thg), sin(2*thg)
    for i in range(len(X)):
        for j in range(len(Y)):
            x,y = X[i],Y[j]
            z[0,j,i] = -gam*x*cs - gam*y*sn
            z[1,j,i] = -gam*x*cs + gam*y*cs
    return z

    
def SIE(gal,X,Y):
    z = zeros((2,len(Y),len(X)))
    re,ell = float(gal[1]), float(gal[2])
    pa = float(gal[3])*pi/180 + pi/2
    #pa = 0.1
    qs = 1-ell*ell
    #pa = 0
    print qs,cos(pa)
    cs,sn = cos(pa),-sin(pa)
    print 'Einstein radius',re
    for i in range(len(X)):
        for j in range(len(Y)):
            x,y = X[i],Y[j]
            x,y = cs*x + sn*y, -sn*x + cs*y
            comp = sqrt((1-qs)/(qs*x*x+y*y))
            ax = re/sqrt(1-qs)*arctan(comp*x)
            ay = re/sqrt(1-qs)*arctanh(comp*y)
            r = sqrt(x*x + y*y + 1e-6)
            #ax = re*x/r
            #ay = re*y/r
            z[0,j,i] = cs*ax - sn*ay
            z[1,j,i] = sn*ax + cs*ay
            #phi = arctan2(y[j],x[i]) - pa
            #comp = s2eps/sqrt(1 - eps*cos(2*phi))
            #z[0,j,i] += re/s2eps * arctan(comp*cos(phi))
            #z[1,j,i] += re/s2eps * arctanh(comp*sin(phi))
            #r = sqrt(x[i]**2 + y[j]**2)
            #z[0,j,i] = re*x[i]/r
            #z[1,j,i] = re*y[j]/r
    return z    

def grids(asw,x,y):
    obj = sim[asw]
    src = obj[1]
    ans = geom(src,x,y)
    ans += shear(obj[3],x,y)
    if obj[0]=='quasar' or obj[0]=='galaxy':
        gal = obj[2]
        ans -= SIE(gal,x,y)
    return ans
    
N = 40
R = 25
x = linspace(-R,R,N)
y = 1*x

fig = figure()
panel = fig.add_subplot(1,1,1)
panel.set_aspect('equal')

# df = grids('ASW0002b6m',x,y)
# df = grids('ASW000102p',x,y)
#df = grids('ASW00019rw',x,y)
# df = grids('ASW0000r8n',x,y)
# df = grids('ASW0001hpf',x,y)
df = grids('ASW0000h2m',x,y)
lev = [0]
panel.contour(x,y,df[0],lev,colors='r')
panel.contour(x,y,df[1],lev,colors='g')

show()
