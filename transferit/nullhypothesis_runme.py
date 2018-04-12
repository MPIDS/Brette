#! /usr/bin/python

import neuron, sys, os, random
foldername = os.getcwd()
from neuron import h
import numpy as np

h('strdef model, codedirectory')
h('load_file("param.hoc")')

sys.path.append(h.codedirectory+'/scripts')
from I_proc_new import stimulate

os.environ.keys()
ii = int(os.environ['SGE_TASK_ID'])
print('ii = %d'%(ii)) # series number in runjobs

N = int(h.T/h.dt)    
dt = h.dt*10**-3   
T = N*dt 
sf = 1/dt 
maxtau = int(0.4*sf) 
L = maxtau*2 

h.T = h.T + h.T_relax

data = np.load('%s/Series%d/spiketimelist.npy'%(foldername, ii))
dic = data.item()
spiketimelist = dic['spiketimelist']

from time import time
fullpath = foldername + '/Series%d'%(ii)
for run in range(1,500+1): # null hypothesis runs
  nspikes = 0
  STA_tmp = np.zeros(L)
  for k in range(len(spiketimelist)):
    start_time = time()
    seednumber = ii*100+k # random seed number for reproducing the stimulus used in runjobs
    stim = stimulate([1,h.mean,h.std,h.tau,h.dt,h.T, seednumber])
    stim = stim[int(500/0.025):]
    random.seed(ii*1000+run) # random seed number for shuffling the spike time
    sp2 = np.sort((spiketimelist[k]+random.uniform(0,20))%20) # add a random number to the spike times and mod them by T=20s
    skipspikeslist = sum(sp2<(maxtau+1)*dt) 
    idxlist = skipspikeslist
    while (len(sp2) > idxlist):
      if (sp2[idxlist]/dt + maxtau < N):
        STA_tmp_add =  stim[(int(sp2[idxlist]/dt)-maxtau-1):(int(sp2[idxlist]/dt)+maxtau-1)] 
        STA_tmp = STA_tmp + np.array(STA_tmp_add)
        idxlist = idxlist + 1
      else: break
    nspikes = nspikes + idxlist - skipspikeslist  
    del stim
    print(time()-start_time)
  STA = STA_tmp/float(nspikes) - h.mean
  np.save(fullpath+'/STA_null_run%d'%(run), {'STA':STA})

