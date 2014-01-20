from numpy import isnan, pi, cos, sin, sqrt, linspace
from pylab import figure, show, savefig, subplots_adjust


lis = open('alist.csv').readlines()[2:]

def re(s):
    return float(s.translate(None,'"'))

def hammer(lam,phi):
    den = 2*sqrt(1+cos(phi)*cos(lam/2))
    hx = -2*cos(phi)*sin(lam/2)/den
    hy = sin(phi)/den
    return hx,hy

def curve(panel,lam,phi):
    x,y = hammer(lam,phi)
    panel.plot(x,y,c='.75')

x = []
y = []
for l in lis:
    s = l.split(',')
    ra = re(s[5])
    dec = re(s[9])
    if not (isnan(dec) or isnan(ra)):
        ra = (ra+180) % 360
        phi = dec*pi/180
        lam = ra*pi/180 - pi
        hx,hy = hammer(lam,phi)
        x.append(hx)
        y.append(hy)

print len(x)

fig = figure()
panel = fig.add_subplot(1,1,1)
N = 20
for phi in linspace(-pi/3,pi/3,5):
    curve(panel,linspace(-pi,pi,20),linspace(phi,phi,N))
for lam in linspace(-pi,pi,13):
    curve(panel,linspace(lam,lam,20),linspace(-pi/2,pi/2,N))

panel.scatter(x,y,c='r',edgecolors='none')

panel.set_aspect('equal')
panel.xaxis.set_visible(False)
panel.yaxis.set_visible(False)
panel.set_xlim(-1,1)
panel.set_ylim(-0.5,0.5)
#show()

# patch to fill whole image, remove white border, use vecort graphics
subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
savefig("lenssky.png", dpi=200, bbox_inches='tight', pad_inches=0)
savefig("lenssky.pdf", dpi=100, bbox_inches='tight', pad_inches=0)
