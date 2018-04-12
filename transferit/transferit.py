#!/usr/bin/python
# Calculation of the linear response function with the STA

import numpy as np
import scipy.io as sio
import math
from neuron import h

hostname = 'chenfei'
model = 'Brette'
runs = 400
datafolder = '/dyn_gain/scratch02/%s/%s/'%(hostname,model)

dt = h.dt*10**-3 # default time step in NEURON is 0.025ms.
sf = 1/dt # sampling frequency
maxtau = int(0.4*sf) 
L = 2*maxtau # STA is 0.8s. The vector length of the STA is 32000.
f = sf/2*np.linspace(0,1,L/2+1) # frequency
idx = 2000 # length of the dynamic gain components to be shown

for tau in (5, ): 
    for (thr,posNa) in ((-35,20),): 
      fr = 5
      appendix = 'tau'+str(tau)+'fr'+str(fr)+'threshold'+str(thr)+'posNa'+str(posNa)
      h('strdef model, codedirectory')
      h('load_file("%s%s/param.hoc")'%(datafolder, appendix)) 
      STA = np.zeros(L)
      for kk in range(1,runs+1):
        datafile = datafolder + appendix + '/Series' + str(kk) + '/STA.npy'
        STA_nspikes = np.load(datafile)
        STA_nspikes_dict = STA_nspikes.item()       
        STA_tmp = STA_nspikes_dict['STA']
        STA = STA + STA_tmp        
      STA = STA/float(runs) # averaged STA over 400 jobs
      sidelength = 0.05
      side = np.arange(0,1+dt/sidelength, dt/sidelength)
      window = np.array(list(side) + list([1]*(L-2*len(side))) + list(1-side))
      STA = STA*window # make the STA begin and end with 0
      ftSTA = np.fft.fft(np.append(STA[L/2:], STA[0:L/2]))/float(L) 
      ftSTA = ftSTA[0:L/2+1] 
      phase = np.angle(ftSTA)      
      psd = 2*tau*(10**-3)*(h.std**2)/(1+(2*math.pi*tau*10**-3*f)**2) # analytical form of the power spectral density of the OU process stimulus
      gain_filt = np.zeros(idx)
      for i in range(idx):
        if i == 0:
          g = np.array([0]*len(ftSTA))
          g[0] = 1
        else:
          g = math.e**(-2*math.pi**2*(f-f[i])**2/f[i]**2) # Gaussian filters, the variance increase with the frequency.
          g = g/float(sum(g))
        gain_filt[i] = abs(sum(ftSTA*g))/float(psd[i]) # filter out the noise in the high frequency components
      if thr<0:
        thr = 'n%d'%(abs(thr))
      else:
        thr = '%d'%(thr)               
      transferdata = {'f':f[range(idx)], 'gain_tau%dfr%dthreshold%sposNa%d'%(tau, fr, thr, posNa):gain_filt}
      sio.savemat(datafolder+'transferdata_tau%dfr%dthreshold%sposNa%d'%(tau, fr, thr, posNa), transferdata)






