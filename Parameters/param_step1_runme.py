#! /usr/nld/python

import neuron, sys, os
from neuron import h
import numpy as np
fullpath = os.getcwd() 
print(fullpath) 
data = np.load('param.npy')
param = data.item()
# parameter sample:
# tau = 5
# thr = -34
# spthr = -35
# posNa = 20
# fr = 5
# T = 20000
# codedirectory = '/home/%s/Code'%(hostname)
# model = 'Brette'
# leftI = 0.00001
# rightI = 0.05
# precisionFiringOnset = 1e-2

# Load parameters. 
for key, val in param.items():
  exec(key + '=val')


sys.path.append('%s/scripts'%(codedirectory))
h('load_file("nrngui.hoc")')                  
h("objref stimulus, stim, APgen, apc, spiketimes, vAIS")
h('thr = %d'%(thr)) 
h("posNa = %f"%(posNa))
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
h('axon apc.record(spiketimes)') # spike time recording
h('axon apc.thresh = %d'%(spthr)) # voltage for spike time detection
h("axon {sodiumchan.loc(posNa/axon_L)}")

# import the function for parameter searching
from firingonset import FiringOnset 

stim_0 = 0
# stim_start: stimulus just about to fire (fr=0Hz)
stim_start = FiringOnset(leftI, rightI, precisionFiringOnset, h.apc, h.stim, T, 0)
# stim_saturate: stimulus that generates 5Hz firing rate (fr=5Hz) 
stim_saturate = FiringOnset(leftI, rightI, precisionFiringOnset, h.apc, h.stim, T, fr) 

# With the constant input stim_saturate, choose the voltage 2ms after the spike detection voltage as the new reset voltage.
from I_proc import stimulate
h('threshold=60')
h('T = 1000')
h('access soma')

h('objref APgen, stimulus, stim, vAIS')
h('axon APgen = new NetCon(&v(posNa/axon_L), sodiumchan,threshold,0,0)')
h('axon {sodiumchan.loc(posNa/axon_L)}')

h.stimulus = h.IClamp(0.5)
h.stimulus.dur = 1e9
h.stimulus.delay = 0
h.stimulus.amp = 0

h.stim = h.Vector()
h('stim.play(&stimulus.amp, dt)')

h('objref apc, spiketimes')
h.apc = h.APCount(0.5) 
h.spiketimes = h.Vector() 
h.apc.record(h.spiketimes)
h.apc.thresh = spthr

h.stim = h.Vector()
h('stim.play(&stimulus.amp, dt)') 
h.finitialize()
h.frecord_init()

h.vAIS = h.Vector(int(T/h.dt)) 
h('vAIS.record(&axon.v(posNa/axon_L))')

h.stim = stimulate([1,h.stim, stim_saturate, 0, tau,h.dt, h.T, 1])
h.apc.n = 0 
h.tstop = h.T
h.run()

va = h.vAIS.to_python()
spthrV = va[np.argmax(np.diff(va)/h.dt)+1]
print("Spike time threshold is %f mV"%(spthrV))
threshold = va[np.argmax(np.diff(va)/h.dt)+1 + int(2/h.dt)]
print("Reset threshold is %f mV"%(threshold))
param['thr'] = int(threshold)
np.save('param',param)
np.save('mean',{'stim_0':stim_0, 'stim_start':stim_start, 'stim_saturate':stim_saturate,})


