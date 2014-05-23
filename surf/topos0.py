import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import get_test_data


def Mask(c):
    
    a = 0*c
    len = np.alen(a)
    l = float(len)
    
    dk = (l-1)/2-0.01
    
    for i in range(0, len):
        for j in range(0, len):
            dx = ((l-1)/2-i)**2
            dy = ((l-1)/2-j)**2
            dis = np.sqrt(dx+dy)
            
            if dis < dk:
                a[i][j] = 1
            else:
                a[i][j] = 0
                
    return a

def Laplace(m):
    
    Genauigkeit = 0.001
    z = np.abs(Genauigkeit)    
    delta = 2    
    repeat = 10000
    
    mas = Mask(m)
    
    konstant = ((1*m)*delta**2)/4    
    kd = 0*m
    k = []
    k.append(kd)
    
    h = 0        
    r = z + 1

    while z < r and repeat > h :
        
        h += 1        
        kd = k[h - 1]
        average = 1*kd
        average[1:-1, 1:-1] = (kd[0: -2, 1: -1] + kd[2:, 1: -1] + kd[1: -1, 0: -2] + kd[1: -1, 2:])/4
        kd = (average + konstant)*mas
        k.append(kd)
    
        if  np.amax(k[h] - k[h-1]) <= z and np.amin(k[h] - k[h-1]) >= -1*z:
            r = 0                
        else:
            r = z + 1
                
    return kd
    
def Phermat(m):
    
    place = Laplace(m)
    xlen = float(len(place))
    ylen = float(len(place))
    xy = 0*place
    
    
    for i in range(len(place)):
        for j in range(len(place[0])):
            xy[i][j] = (xlen/2-i)**2+(ylen/2-j)**2
    
    pherma = place + xy
    
    return pherma
    
def Maskb(c):
    
    a = c
    len = np.alen(a)
    l = float(len)
    
    dk = (l-1)/2-0.01
    
    for i in range(0, len):
        for j in range(0, len):
            dx = ((l-1)/2-i)**2
            dy = ((l-1)/2-j)**2
            dis = sqrt(dx+dy)
            
            if dis < dk:
                pass
            else:
                a[i][j] = None
                
    return a    
    

spag = 0

ma = np.zeros((100,100), float)
levs = [1620]
dt = 55
if spag==1:
    ma[45: 52, 45: 52] = 25
    levs = [1211]
if spag==2:
    ma[45: 50, 30: 70] = 10


        
h = Phermat(ma)

side = h[0,50]
for i in range(len(h)):
    for j in range(len(h)):
        dh = h[i,j] - side
        if dh > 0:
            h[i,j] = side
        

bgcol = '0.5'

fig = plt.figure(facecolor=bgcol)
ax = fig.add_subplot(1, 1, 1, projection='3d', axisbg=bgcol)  # 3D
ax.axis('off')

X = np.arange(100)
Y = np.arange(100)
X, Y = np.meshgrid(X, Y)

ax.axis('equal')

lo = np.amin(h)
hi = np.amax(h)

while True:
    v = levs[0]-dt
    if v < lo:
        break
    levs = [v] + levs
while True:
    v = levs[-1]+dt
    if v+2*dt > hi:
        break
    levs = levs + [v]

surf = plt.contour(X, Y, h, levs, cmap=cm.gist_rainbow)

plt.show()

