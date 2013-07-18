from numpy import pi,cos,arctan2,arctan,arctanh,sqrt

def kappa_NFW(x,y,gx,gy,kappa,rscale,ell,ell_pa):
    pa = ell_pa*180/pi + pi/2
    x,y = x-gx,y-gy
    phi = arctan2(y,x) - pa
    th2r = x*x + y*y + 1e-6
    th2p = 1 - ell*cos(2*phi)
    r = sqrt(th2r*th2p)
    u = r/rscale
    if u==1.:
        f = 1./3
    else:
        if u < 1:
            f = 1 - 2/sqrt(1-u*u) * arctanh(sqrt((1-u)/(1+u)))
        else:
            f = 1 - 2/sqrt(u*u-1) * arctan(sqrt((u-1)/(u+1)))
        f /= (u*u-1)
    return kappa*f

    
