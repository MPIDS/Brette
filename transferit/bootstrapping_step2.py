#!/usr/bin/python
import numpy as np
import scipy.io as sio

hostname = 'chenfei'
model = 'Brette'
runs = 1000
datafolder = '/dyn_gain/scratch01/%s/%s/'%(hostname, model)

for tau in (5, ): 
  for (thr,posNa) in ((-23,20),):
    fr = 5 
    appendix = 'tau'+str(tau)+'fr'+str(fr)+'threshold'+str(thr)+'posNa'+str(posNa)
    foldername = datafolder + appendix
    gain = []
    for i in range(1,runs+1):
      data = np.load(datafolder+appendix+'/bootstrapping/transferdata_bootstrapping_%d.npy'%(i))
      dic = data.item()
      gain.append(dic['gain'])
    
    gain_all = np.array(gain)
    gain = np.sort(gain_all, axis=0)
    bootstrapping_gain_lower = gain[int(runs*0.025)] # take the 95 percent in the middle as the confidence interval
    bootstrapping_gain_upper = gain[int(runs*0.975)]
    if thr<0:
      thr = 'n%d'%(abs(thr))
    else:
      thr = '%d'%(thr)
    data_appendix = 'tau%dfr%dthreshold%sposNa%d'%(tau, fr, thr, posNa)
    data = sio.loadmat(datafolder+'transferdata_%s.mat'%(data_appendix))
    data['bootstrapping_gain_lower_%s'%(data_appendix)] = bootstrapping_gain_lower
    data['bootstrapping_gain_upper_%s'%(data_appendix)] = bootstrapping_gain_upper
    data['gain_all'] = gain_all
    sio.savemat(datafolder+'transferdata_%s'%(data_appendix), data)
