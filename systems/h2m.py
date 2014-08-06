from numpy import zeros, linspace, amin, amax, sqrt, pi, cos, sin, arctan, arctanh, arctan2
from pylab import figure, show
from many import grids

from matplotlib import rc
rc('text', usetex=True)


def readq():
    sim = {}
    fil = open('../catalogs/cfhsimcat.txt')
    all = fil.readlines()
    for l in all:
        if l[:3] == 'ASW':
            s = l.split()
            gid = s[1]
            sim[gid] = [s[0],s[-1]]
    fil = open('../catalogs/simcat_q.txt')
    all = fil.readlines()
    for k,l in enumerate(all):
        if k > 2:
            s = l.split()
            gid = s[0]
            sim[gid].append(('source',s[16],s[17]))
            sim[gid].append(('SIE',s[13],s[11],s[12]))
            sim[gid].append(('ext shear',s[14],s[15]))
    tidy = {}
    for gid in sim:
        s = sim[gid]
        if s[0] != 'ASW0001gae':
            tidy[s[0]] = s[1:]
    return tidy

def alpha_SIE(x,y,reinst,ell,ell_pa):
    pa = ell_pa*pi/180 + pi/2
    q = 1 - ell
    cs,sn = cos(pa),sin(pa)
    x,y = cs*x + sn*y, -sn*x + cs*y
    A = reinst*q/sqrt(1-q*q)
    B = sqrt((1-q*q)/(q*q*x*x +y*y))
    phix = A*arctan(B*x)
    phiy = A*arctanh(B*y)
    return (phix,phiy)

def alpha_shear(x,y,sh_str,sh_pa):
    thg = sh_pa*pi/180 + pi/2
    r = sqrt(x*x + y*y)
    f = arctan2(y,x) - 2*thg
    return (-sh_str*r*cos(f),sh_str*r*sin(f))

def far(asw,x,y):
    dx = zeros((len(y),len(x)))
    dy = 1*dx
    obj = sim[asw]
    src = obj[1]
    bx,by = float(src[1]), float(src[2])
    gal = obj[2]
    reinst,ell,ell_pa = float(gal[1]), float(gal[2]), float(gal[3])
    print reinst,ell,ell_pa
    xs = obj[3]
    sh_str,sh_pa = float(xs[1]), float(xs[2])
    for i in range(len(x)):
        for j in range(len(y)):
            phix,phiy = alpha_SIE(x[i],y[j],reinst,ell,ell_pa)
            shx,shy = alpha_shear(x[i],y[j],sh_str,sh_pa)
            r = sqrt(x[i]**2+y[j]**2)
            dx[j,i] = bx - x[i] + reinst*x[i]/r
            dy[j,i] = by - y[j] + reinst*y[j]/r
    return dx*dx + dy*dy



sim = readq()

print sim['ASW0000h2m']
N,R = 100,20
x = linspace(-R,R,N)
y = 1*x
# kappa,arriv = grids('ASW0000h2m',x,y)
lum = far('ASW0000h2m',x,y)
fig = figure()
panel = fig.add_subplot(1,1,1)
panel.set_aspect('equal')
# lo,hi = amin(lum), amax(lum)
lev = linspace(-0.01,0.01,10)
panel.contour(x,y,lum,lev)
#panel.contour(x,y,lum[0],lev)
#panel.contour(x,y,lum[1],lev)
show()

