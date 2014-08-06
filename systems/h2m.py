from numpy import linspace, amin, amax, cos, arctan2
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
    rsq = x*x + y*y
    f = arctan2(y,x) - 2*thg
    return (-sh_str*r*cos(f),sh_str*r*sin(f))

def disp(asw,x,y):
    obj = sim[asw]

sim = readq()

print sim['ASW0000h2m']
N,R = 100,20
x = linspace(-R,R,N)
y = 1*x
kappa,arriv = grids('ASW0000h2m',x,y)
fig = figure()
panel = fig.add_subplot(1,1,1)
panel.set_aspect('equal')
lo,hi = amin(arriv), amax(arriv)
lev = linspace(lo,lo+.2*(hi-lo),100)
panel.contour(x,y,arriv,lev)
show()

