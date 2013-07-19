from numpy import sqrt,pi,cos,sin,arctan2,arctan,arctanh,log

# See eqns (34,35) from Keeton astro-ph/0102341
def poten_SIE(x,y,reinst,ell,ell_pa):
    pa = ell_pa*pi/180 + pi/2
    q = 1 - ell
    cs,sn = cos(pa),sin(pa)
    x,y = cs*x + sn*y, -sn*x + cs*y
    A = reinst*q/sqrt(1-q*q)
    B = sqrt((1-q*q)/(q*q*x*x +y*y))
    phix = A*arctan(B*x)
    phiy = A*arctanh(B*y)
    return x*phix + y*phiy

# See eqn (10) from Keeton et al 2000ApJ...537..697K
def poten_shear(x,y,sh_str,sh_pa):
    thg = sh_pa*pi/180 + pi/2
    rsq = x*x + y*y
    f = 2*(arctan2(y,x) - thg)
    return -sh_str/2*rsq*cos(f)

# See eqns (48,50) from Keeton astro-ph/0102341
def poten_NFW(x,y,kaps,rsc):
    u = sqrt(x*x+y*y+1e-6)/rsc
    if u>1:
        v = sqrt(u*u-1)
        F = arctan(v)/v
    if u<1:
        v = sqrt(1-u*u)
        F = arctanh(v)/v
    return kaps*rsc*rsc * (log(u*u/4) + 2*F)