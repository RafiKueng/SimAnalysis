from numpy import sqrt,pi,cos,arctan2,arctan,arctanh

def kappa_SIE(x,y,reinst,ell,ell_pa):
    pa = ell_pa*pi/180 + pi/2
    phi = arctan2(y,x) - pa
    r = sqrt( (x*x + y*y + 1e-6) * (1 - ell*cos(2*phi)) )
    return reinst/r
    
def poten_shear(x,y,sh_str,sh_pa):
    thg = sh_pa*pi/180 + pi/2
    rsq = x*x + y*y
    f = 2*(arctan2(y,x) - thg)
    return -sh_str/2*rsq*cos(f)

def kappa_NFW(x,y,gx,gy,kappa,rscale,ell,ell_pa):
    pa = ell_pa*180/pi + pi/2
    x,y = x-gx,y-gy
    phi = arctan2(y,x) - pa
    r = sqrt( (x*x + y*y + 1e-6) * (1 - ell*cos(2*phi)) )
    u = r/rscale
    if u==1.:
        f = 1./3
    else:
        if u < 1:
            f = 1 - 2/sqrt(1-u*u) * arctanh(sqrt((1-u)/(1+u)))
        else:
            f = 1 - 2/sqrt(u*u-1) * arctan(sqrt((u-1)/(u+1)))
        f /= (u*u-1)
    return 2*kappa*f

    
