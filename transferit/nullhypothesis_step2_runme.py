#!/usr/bin/python

import neuron, os, math
import numpy as np
from neuron import h

os.environ.keys()
ii = int(os.environ['SGE_TASK_ID'])
print('ii = %d'%(ii)) # null hypothesis run index

fullpath = os.getcwd()
h('strdef model, codedirectory')
h('load_file("param.hoc")')

runs = 400 # runjob series number
dt = h.dt*10**-3
sf = 1/dt
maxtau = int(0.4*sf)
L = 2*maxtau
f = sf/2*np.linspace(0,1,L/2+1)
idx = 2000
STA = np.zeros(L)

for kk in range(1,runs+1):
  datafile = fullpath + '/Series' + str(kk) + '/STA_null_run%d.npy'%(ii)
  data = np.load(datafile)
  dic = data.item() # It contains paramstr, STA_kk, and nspikes.      
  STA_tmp = dic['STA']
  STA = STA + STA_tmp

      
STA = STA/float(runs)   
sidelength = 0.05
side = np.arange(0,1+dt/sidelength, dt/sidelength) 
window = np.array(list(side) + list([1]*(L-2*len(side))) + list(1-side)) 
STA = STA*window
ftSTA = np.fft.fft(np.append(STA[L/2:], STA[0:L/2]))/float(L) 
ftSTA = ftSTA[0:L/2+1]  
psd = 2*h.tau*(10**-3)*(h.std**2)/(1+(2*math.pi*h.tau*10**-3*f)**2) 
gain_filt = np.zeros(idx)
for i in range(idx):
  if i == 0:
    g = np.array([0]*len(ftSTA))
    g[0] = 1
  else:
    g = math.e**(-2*math.pi**2*(f-f[i])**2/f[i]**2) 
    g = g/float(sum(g))
  gain_filt[i] = abs(sum(ftSTA*g))/float(psd[i])


transferdata = {'f':f[range(idx)], 'gain':gain_filt}
np.save('nullhypothesis/transferdata_nullhypothesis_run%d'%(ii), transferdata)





