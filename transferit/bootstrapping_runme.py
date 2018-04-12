#!/usr/bin/python

import os, math
from subprocess import call
import numpy as np
from neuron import h
from random import randint


os.environ.keys()
ii = int(os.environ['SGE_TASK_ID'])
print('ii = %d'%(ii))

runs = 400
datafolder = os.getcwd()

dt = h.dt*10**-3 # Here default h.dt is 0.025ms in NEURON.
sf = 1/dt
maxtau = int(0.4*sf)
L = 2*maxtau
f = sf/2*np.linspace(0,1,L/2+1) 
idx = 2000

for tau in (5, ):  
    for (thr,posNa) in ((-23,20),): 
      fr = 5
      appendix = 'tau'+str(tau)+'fr'+str(fr)+'threshold'+str(thr)+'posNa'+str(posNa)
      h('strdef model, codedirectory')
      h('load_file("%s/%s/param.hoc")'%(datafolder, appendix)) 
      STA = np.zeros(L)
      for kk in [randint(1,runs) for i in range(runs)]: # randomly select 400 STA from the data set with replacement
        datafile = datafolder + '/' + appendix + '/Series' + str(kk) + '/STA.npy'
        STA_nspikes = np.load(datafile)
        STA_nspikes_dict = STA_nspikes.item()       
        STA_tmp = STA_nspikes_dict['STA']
        STA = STA + STA_tmp    
      STA = STA/float(runs) # calculate the linear response curve with the new STA
      sidelength = 0.05
      side = np.arange(0,1+dt/sidelength, dt/sidelength)
      window = np.array(list(side) + list([1]*(L-2*len(side))) + list(1-side)) 
      STA = STA*window
      ftSTA = np.fft.fft(np.append(STA[L/2:], STA[0:L/2]))/float(L) 
      ftSTA = ftSTA[0:L/2+1] 
      psd = 2*tau*(10**-3)*(h.std**2)/(1+(2*math.pi*tau*10**-3*f)**2)
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
      if os.path.isdir(datafolder+'/%s/bootstrapping'%(appendix)) == False:
        os.mkdir(datafolder+'/%s/bootstrapping'%(appendix))
      np.save(datafolder+'/%s/bootstrapping/transferdata_bootstrapping_%d'%(appendix,ii), transferdata)






