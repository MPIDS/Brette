#! /usr/bin/python

import neuron, sys, os
from neuron import h
import numpy as np
fullpath = os.getcwd()
print(fullpath)
# Parameters loading
data = np.load('mean.npy')
dic = data.item()
stim_0 = dic['stim_0']  
stim_start = dic['stim_start'] 
stim_saturate = dic['stim_saturate'] 
# Or you can define parameters by hand
# stim_0 = 
# stim_start = 
# stim_saturate = 

data = np.load('param.npy')
param = data.item()
for key, val in param.items():
  exec(key + '=val')


os.environ.keys()
i = int(os.environ['SGE_TASK_ID'])
print('i = %d'%(i))

if i<101:
  mean = (stim_start - stim_0)/100*(i-1) + stim_0 # assign 100 data points between stim_0 and stim_start
else:
  mean = (stim_saturate - stim_start)/100*(i-101) + stim_start # assign 100 data points between stim_start and stim_saturate


sys.path.append('%s/scripts'%(codedirectory))
h('load_file("nrngui.hoc")')                   
h("objref stimulus, stim, apc, spiketimes, APgen")
h("posNa = %f"%(posNa))
h('thr = %d'%(thr))
h.load_file("%s/Mechanism/%s/Neuron.hoc"%(codedirectory, model))

h('access soma')
h.stimulus = h.IClamp(0.5) 
h.stimulus.dur = 1e9
h.stimulus.delay = 0
h.stimulus.amp = 0

h.stim = h.Vector() 
h("stim.play(&stimulus.amp, dt)")

h('access axon')
h("axon APgen = new NetCon(&v(posNa/axon_L), sodiumchan,thr,0,0)") 
h('axon apc = new APCount(posNa/axon_L)')
h('axon spiketimes = new Vector()')
h('axon apc.record(spiketimes)')
h('axon apc.thresh = %d'%(spthr)) 
h("axon {sodiumchan.loc(posNa/axon_L)}")

# import the function for parameter searching
from Determinestd import DetermineStdI

leftStd = 0.00000001 # lowerbound
rightStd = 0.08 # upperbound
precision_std = 1e-3 # relative error for parameter searching
seednumber = i
std = DetermineStdI(leftStd, rightStd, precision_std, h.apc, mean, h.stim, tau, h.dt, 10*T, fr,seednumber) # Searching for std. Simulation time is 200s.
sp = h.spiketimes.to_python() # obtain the spike times from the iteration in DetermineStdI 
isi = np.diff(sp)
cv = np.std(isi)/np.mean(isi) # estimate the CV of ISI 
print('cv is %f'%(cv))

np.save('%s/mean%d/std_mean_cv'%(fullpath, i),{'mean':mean, 'std':std, 'cv':cv})


