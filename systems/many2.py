from numpy import linspace, zeros, amin, amax, sqrt, pi, gradient
import numpy as np
from pylab import contour, figure, savefig, show
from poten import poten_SIE, poten_NFW, poten_shear
from angdiam import dratio
import matplotlib as mpl

import os

from scipy import ndimage

from matplotlib import rc
rc('text', usetex=True)
# rc('font', family='serif')

import params
sim = params.read()

def geom(src,x,y):
    z = zeros((len(y),len(x)))
    bx,by = float(src[1]), float(src[2])
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = ((x[i]-bx)**2 + (y[j]-by)**2)/2
    return z


def shear(xs,x,y):  
    z = zeros((len(y),len(x)))
    sh,pa = float(xs[1]), float(xs[2])
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = poten_shear(x[i],y[j],sh,pa)
    return z


def poten_gal(gal,x,y):
    z = zeros((len(y),len(x)))
    re,ell,ell_pa = float(gal[1]), float(gal[2]), float(gal[3])
    #print 'Einstein radius',re
    #print 'ellipticity',ell
    #print 'pos ang',ell_pa
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = poten_SIE(x[i],y[j],re,ell,ell_pa)
    return z

def poten_clus(clus,zsrc,x,y):
    z = zeros((len(y),len(x)))
    kaps = float(clus[0][1])
    rsc = float(clus[0][2])
    zlens = float(clus[1][3])
    fudge = dratio(zlens,zsrc)
    #print 'kaps,rsc',kaps,rsc
    for i in range(len(x)):
        for j in range(len(y)):
            z[j,i] = fudge * poten_NFW(x[i],y[j],kaps,rsc)
    for g in range(1,len(clus)):
        gal = clus[g]
        gx,gy = float(gal[1]), float(gal[2])
        zlens = float(gal[3])
        fudge = dratio(zlens,zsrc)
        sig = float(gal[4])
        #print 'sigma', sig
        ell,pa = float(gal[5]),float(gal[6])
        reinst = 4*pi*(sig/3e5)**2 * 206265/.186 * fudge
        #print 'pos',gx,gy
        #print 'reinst,ell,pa',reinst,ell,pa
        for i in range(len(x)):
            for j in range(len(y)):
                z[j,i] += poten_SIE(x[i]-gx,y[j]-gy,reinst,ell,pa)
    return z

def grids(asw,x,y):
    obj = sim[asw]
    basic = geom(obj[1],x,y)
    if obj[0]=='quasar' or obj[0]=='galaxy':
        gal = obj[2]
        poten = poten_gal(gal,x,y)            
        basic -= shear(obj[3],x,y)
    else:
        zsrc = float(obj[1][-1])
        clus = obj[2]
        poten = poten_clus(clus,zsrc,x,y) 
    kappa = 0*poten
    kappa[1:-1,1:-1] = poten[0:-2,1:-1] + poten[2:,1:-1] \
                     + poten[1:-1,0:-2] + poten[1:-1,2:] \
                     - 4*poten[1:-1,1:-1]
    dx = x[1]-x[0]
    kappa /= 2*dx*dx
    return (kappa,basic-poten)

def draw(asw):
    print "\n    '%s':["%asw
    N,R = 200,50
    if sim[asw][0] == 'quasar':
        flag,R = 'Q',20
    if sim[asw][0] == 'galaxy':
        flag,R = 'G',20
    if sim[asw][0] == 'cluster':
        flag,R = 'C',50
    x = linspace(-R,R,N)
    y = 1*x
    kappa,arriv = grids(asw,x,y)
    #fig = figure()
    #panel = fig.add_subplot(1,1,1)
    #panel.set_aspect('equal')
    lev = linspace(0,10,41)
    #pc = panel.contour(x,y,kappa,lev)
    #panel.clabel(pc, inline=1, fontsize=10)
    #savefig(folder+asw+flag+'_kappa.png')
    #fig = figure()
    #panel = fig.add_subplot(1,1,1)
    rad = linspace(0,R,20)[1:]
    radq = rad*rad
    sum = 0*rad
    for i in range(len(x)):
        for j in range(len(y)):
            rsq = x[i]**2 + y[j]**2
            for k in range(len(rad)):
                if rsq < radq[k]:
                    sum[k] += kappa[j,i]
    dx = x[1]-x[0]
    for k in range(len(rad)):
        sum[k] *= dx*dx/(pi*radq[k])
    #fil = open('figs/'+asw+'.txt','w')
    #for k in range(len(rad)):
    #    fil.write('%9.2e %9.2e\n' % (rad[k],sum[k]))
    #fil.close()
    #panel.scatter(rad,sum)
    #panel.set_xlabel('radius in pixels')
    #panel.set_ylabel('average interior $\kappa$')
    #savefig(folder+asw+flag+'_menc.png')
    
    
    #arriv = upsample(x,y,arriv, upsample=10)
    x1, y1 = gradient(arriv)
    #print 'x1',x1
    #x1, y1 = np.abs(x1), np.abs(y1)
    sig = 1
    x1 = ndimage.gaussian_filter(x1, sigma=sig, mode='wrap')
    y1 = ndimage.gaussian_filter(y1, sigma=sig, mode='wrap')
    
        
    
    z1 = x1*x1+y1*y1
    #z1 = ndimage.gaussian_filter(z1, sigma=3)

    z1 = ndimage.gaussian_gradient_magnitude(arriv, sigma=sig, mode='nearest')
    #z2 = ndimage.laplace(arriv)    
    
    #zmin = amin(z1) * 42. # because it's 42
    #print 'zmin',zmin
    #mask = z1<zmin
    mask, ids = detect_local_minima(np.log(z1))
    
    typestr = {
      -2: 'bg',
      -1: 'udef',
      0: 'sad',
      1: 'min',
      2: 'max',
      3: 'canc'}
      
    types, s1, s2 = def_type(ids, x1,y1)
    #print types
    
    ids, types, s1, s2 = filter_types(ids, types, s1, s2, thres=10)
    #print types
    
    pnttype = np.ones(mask.shape) * -2
    xids, yids = ids
    #print ids
    for i, xx in enumerate(xids):
      yy=yids[i]
      t=types[i]
      #print i, xx, yy, t, typestr[t], s1[i], s2[i], arriv[xx,yy]
      print "        %f, # %i, %s" % (arriv[xx,yy], i, typestr[t])
      
      pnttype[xx,yy]=t
    print "    ],"
    
    #return mask
    if False:
      fig = figure()
      panel = fig.add_subplot(2,2,1)
      panel.imshow(np.log(z1),origin='lower',interpolation='nearest')
      #panel.streamplot(x-np.min(x),y-np.min(y),y1,x1, density=5, minlength=0.01)
      panel = fig.add_subplot(2,2,2)
      panel.imshow(mask,origin='lower', vmin=0, vmax=1,interpolation='nearest')
      panel = fig.add_subplot(2,2,3)
      panel.imshow(x1,origin='lower',interpolation='nearest')
      panel = fig.add_subplot(2,2,4)
      panel.imshow(pnttype,origin='lower',interpolation='nearest')
      show()
      #savefig(folder+asw+flag+'_derr.png')

    if False:
        fig = figure()
        panel = fig.add_subplot(1,1,1)
        panel.imshow(np.log(z1),origin='lower',interpolation='nearest', cmap='binary')
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['black','blue','yellow', 'red', 'green', 'magenta'],6)    
        cmap1._init()
        cmap1._lut[:,-1] = np.array([0,1,1,1,1,1,1,1,1])
        panel.imshow(pnttype,origin='lower',interpolation='nearest', cmap=cmap1, vmin=-2, vmax=+3)
        os.mkdir(os.path.join(folder,asw))
        savefig(os.path.join(folder,asw,'extr_points.png'))


    '''
    fig = figure()
    panel = fig.add_subplot(1,1,1)
    #panel.imshow(mask,origin='lower', vmin=0, vmax=1, interpolation='nearest')
    panel.imshow(np.log(z1),origin='lower',interpolation='nearest')
#    panel = fig.add_subplot(2,1,2)
#    panel.imshow(y)
    #show()
    savefig(folder+asw+flag+'_derr.png')
      ''' 
    
    if False:
        fig = figure()
        panel = fig.add_subplot(1,1,1)
        panel.set_aspect('equal')
        lo,hi = amin(arriv), amax(arriv)
        lev = linspace(lo,lo+.2*(hi-lo),100)
        panel.contour(x,y,arriv,lev)
        savefig(folder+asw+flag+'_arriv.png')
    
    
    if False:
      fig = figure()
      panel = fig.add_subplot(1,1,1)
      panel.set_aspect('equal')
      lo,hi = amin(arriv), amax(arriv)
      lev = linspace(lo,lo+.2*(hi-lo),100)
      
      f = 2.5 if not flag=='C' else 1
      
      panel.imshow(np.log(z1),origin='lower',interpolation='nearest', cmap='binary')
      panel.contour((x+R)*f,(y+R)*f,arriv,lev)
      panel.imshow(pnttype,origin='lower',interpolation='nearest', cmap=cmap1, vmin=-2, vmax=+3)
      
      #show()
      savefig(folder+asw+flag+'_all.png')
        
    

import scipy.ndimage.filters as filters
import scipy.ndimage.morphology as morphology

def detect_local_minima(arr):
    # http://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array/3689710#3689710
    """
    Takes an array and detects the troughs using the local maximum filter.
    Returns a boolean mask of the troughs (i.e. 1 when
    the pixel's value is the neighborhood maximum, 0 otherwise)
    """
    # define an connected neighborhood
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#generate_binary_structure
    #neighborhood = morphology.generate_binary_structure(len(arr.shape),connectivity=30)
    r = 3
    mx, my = np.ogrid[-r:r+1, -r:r+1]
    mask = mx*mx+my*my <= r*r
    neighborhood = mask
    #neighborhood = np.ones((10,10))
    #print 'nh:', arr.shape, len(arr.shape)
    #print neighborhood
    # apply the local minimum filter; all locations of minimum value 
    # in their neighborhood are set to 1
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.filters.html#minimum_filter
    local_min = (filters.minimum_filter(arr, footprint=neighborhood)==arr)
    # local_min is a mask that contains the peaks we are 
    # looking for, but also the background.
    # In order to isolate the peaks we must remove the background from the mask.
    # 
    # we create the mask of the background
    background = (arr==0)
    # 
    # a little technicality: we must erode the background in order to 
    # successfully subtract it from local_min, otherwise a line will 
    # appear along the background border (artifact of the local minimum filter)
    # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#binary_erosion
    eroded_background = morphology.binary_erosion(
        background, structure=neighborhood, border_value=1)
    # 
    # we obtain the final mask, containing only peaks, 
    # by removing the background from the local_min mask
    detected_minima = local_min - eroded_background

    #remove border
    lx, ly = np.shape(arr)
    for x in range(lx):
      detected_minima[x,0]=False
      detected_minima[x,ly-1]=False
    for y in range(ly):
      detected_minima[0,y]=False
      detected_minima[lx-1,y]=False
      
      
    return detected_minima, np.where(detected_minima)  
    #return np.where(detected_minima)  


def upsample(x, y, arr, upsample=4):
  xdim, ydim = np.shape(arr)
  #print 'old:', np.shape(arr), 
  xvec = np.linspace(0, 1, xdim)
  yvec = np.linspace(0, 1, ydim)
  from scipy.interpolate import RectBivariateSpline
  interpol = RectBivariateSpline(xvec, yvec, arr)
  
  xnew = np.linspace(0, 1, upsample*xdim)
  ynew = np.linspace(0, 1, upsample*ydim)
  
  new = interpol(xnew, ynew) 
  #print 'new:', np.shape(new)
  return new
    
    
def proj(a,b):
  '''projects vector b onto vector a, gives length of projection
  this is basically the scalarproduct / a
  a, b are complex
  '''
  return np.linalg.norm(b) * np.cos(np.angle(b)-np.angle(a))
  
def def_type(extr_list, dx, dy):
  ''' determines for each extrema with ids from extr_list, in arr
  what type it is
  0 = sad
  1 = min
  2 = max
  returns list with type for each id
  '''
  res = []
  res_s = []
  res_s2 = []
  poss = [3,3+1j, 2+2j, 1+3j, 3j, -1+3j, -2+2j, -3+1j]
  poss.extend([-1*_ for _ in poss])
  xids, yids = extr_list
  for i, x1 in enumerate(xids):
    y1 = yids[i]
    v1 = complex(x1,y1)
    s = 0
    s2 = 0
    for v2 in poss:
      x2, y2 = v2.real, v2.imag
      v3 = v1+v2 #the pos of the pixel
      x4 = dx[v3.real, v3.imag] #the gradient at that pixel
      y4 = dy[v3.real, v3.imag] #the gradient at that pixel
      v4 = complex(x4,y4)
      val = proj(v2, v4)
      s+= 1 if val>0 else -1
      s2 += val
    if s>=15: t=1 #min
    elif s<=-15: t=2 #max
    elif np.abs(s)<=14: t=0
    else: t=-1 #undef
    res.append(t)
    res_s.append(s)
    res_s2.append(s2)
    
    if 0:
      print v1, s, t, s2, 
      if   t==-1: print 'udef'
      elif t==0: print 'sad'
      elif t==1: print 'min'
      elif t==2: print 'max'
  return res, res_s, res_s2




def filter_types(ids, types, s1, s2, thres=10):
  '''very ugly code..
  filters out points of the same type that are too close each other'''
  
  xids, yids = ids
  vals = {-1:[], 0:[], 1:[], 2:[]}
  for i, xid in enumerate(xids):
    yid=yids[i]
    t=types[i]
    ss1=s1[i]
    ss2=s2[i]
    vals[t].append([xid, yid, ss1, ss2, True])
    
  #print vals
  
  for t in range(0,3):
    n = len(vals[t])
    if t==2: comp = lambda x,y:  x>y
    if t==1: comp = lambda x,y:  x<y
    if t==0: comp = lambda x,y: np.abs(x)>np.abs(y)
    for i in range(n):
      #print t, i, vals[t][i]
      x1,y1,s11,s21,_ = vals[t][i]
      for j in range(i+1,n):
        x2,y2,s12, s22, _ = vals[t][j]
        dx = x1-x2
        dy = y1-y2
        if dx*dx+dy*dy<thres*thres:
                    
          if comp(s21, s22): vals[t][i][4] = False
          else: vals[t][j][4] = False
          
  #print vals
  
  res_x = []
  res_y = []
  res_t = []
  res_s1 = []
  res_s2 = []
  
  for typ, val in vals.items():
    for x,y,s1,s2,_ in val:
      res_x.append(x)
      res_y.append(y)
      res_s1.append(s1)
      res_s2.append(s2)
      res_t.append(typ if _ else 3)
  
  return ((res_x, res_y), res_t, res_s1, res_s2)
      
  
        
  
    
folder = 'figs3/'
for asw in sim:
    #print asw
    #if not asw.endswith('0kad'): continue
    draw(asw)
    #break


