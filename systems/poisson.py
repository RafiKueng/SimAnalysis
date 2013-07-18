from numpy import zeros, amax, amin, sqrt
import numpy as np

def Mask(c):
    
    a = 0*c
    len = np.alen(a)
    l = float(len)
    
    dk = (l-1)/2-0.01
    
    for i in range(0, len):
        for j in range(0, len):
            dx = ((l-1)/2-i)**2
            dy = ((l-1)/2-j)**2
            dis = sqrt(dx+dy)
            
            if dis < dk:
                a[i][j] = 1
            else:
                a[i][j] = 0
    return a

def Laplace(m):
    
    Genauigkeit = 0.0001  
    
    repeat = 40000
    
    mas = Mask(m)
      
    kd = 0*m
    
    h = 0

    while repeat > h :
        
        h += 1        
        average = 0*kd
        average[1:-1, 1:-1] = (kd[0: -2, 1: -1] + kd[2:, 1: -1] + kd[1: -1, 0: -2] + kd[1: -1, 2:])/4
        kold = 1*kd
        kd = kd + ((average + m/4)*mas - kd)
    
        diff = amax(abs(kd - kold))
        if h%1000 == 0:
            print h, diff
        if diff < Genauigkeit:
            break

    return kd
    
    
