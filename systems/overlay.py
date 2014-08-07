from matplotlib import rc
rc('text', usetex=True)

from numpy import linspace, amin, amax
from pylab import imshow, figure, show
from matplotlib.image import imread

import params
import many

sim = params.read()

def draw(asw,xc,yc):
    print asw
    N,R = 100,50
    if sim[asw][0] == 'quasar':
        flag,R = 'Q',20
    if sim[asw][0] == 'galaxy':
        flag,R = 'G',20
    if sim[asw][0] == 'cluster':
        flag,R = 'C',42
    x = linspace(-R,R,N)
    y = 1*x
    kappa,arriv = many.grids(asw,x,y)
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    panel.set_aspect('equal')
    swsquare = imread('asw/'+asw+'.png')
    panel.imshow(swsquare[yc-R:yc+R+1,xc-R:xc+R+1])
    lo,hi = amin(arriv), amax(arriv)
    lev = linspace(lo,lo+.2*(hi-lo),100)
    x = 1.2*x
    y = 1.2*y
    panel.contour(x+R,-y+R,arriv,lev)
    show()

draw('ASW000102p',392,244)
draw('ASW0001hpf',379,330)
draw('ASW0004oux',43,183)
draw('ASW0000vqg',341,61)
draw('ASW000195x',316,340)
draw('ASW0002z6f',250,139)
draw('ASW0000h2m',59,67)





