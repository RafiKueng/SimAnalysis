from scipy.integrate import odeint

Omr = 4.8e-5
Omm, Oml = 0.3, 0.7
Omk = 1 - Omm - Omr - Oml

def dcomov(r,a):
    H = (Omm/a**3 + Omr/a**4 + Oml + Omk/a**2)**.5
    return 1/(a*a*H)

def dratio(zlens,zsrc):
    alens = 1./(1+zlens)
    asrc = 1./(1+zsrc)
    a = [asrc,alens,1]
    r = odeint(dcomov,[0],a)[:,0]
    return r[1]/r[2]

