#! /usr/bin/python

import os, neuron, sys
from neuron import h
import numpy as np
import scipy.io as sio

hostname = 'chenfei'
model = 'Brette' # model name
h('dt=0.025') # time step (ms)
h('tau=5') # correlation time of the stimulus (ms)
h('posNa=20') # position of the sodium channels (um)
h('T=1000') # simulation time (ms)
h('threshold=-23') # axonal voltage reset threhold (mV)
stim_mean = 0.0185 # mean of the stimulus (nA)
stim_std = 0.046 # std of the stimulus (nA)

sys.path.append('/home/%s/Code/scripts'%(hostname))
h('load_file("nrngui.hoc")')
tmp_str = '/home/%s/Code/Mechanism/%s/Neuron.hoc'%(hostname, model)
h.load_file(tmp_str) # Load the neuron model.
from I_proc import stimulate # stimulus generation function

h('access soma')
h('objref APgen, stimulus, stim, vAIS, vSoma, m')
h('axon APgen = new NetCon(&v(posNa/axon_L), sodiumchan,threshold,0,0)')
h('axon {sodiumchan.loc(posNa/axon_L)}') # Insert sodium channels in axon.
 
h.stimulus = h.IClamp(0.5) # The stimulus is injected in the middle of the soma.
h.stimulus.dur = 1e9
h.stimulus.delay = 0
h.stimulus.amp = 0
h.stim = h.Vector()
h('stim.play(&stimulus.amp, dt)') 
h.finitialize()
h.frecord_init()

# Recording of the axonal voltage, somatic voltage and sodium activation variable
h.vAIS = h.Vector(int(h.T/h.dt)) 
h.vSoma = h.Vector(int(h.T/h.dt))
h.m = h.Vector(int(h.T/h.dt))
h('vAIS.record(&axon.v(posNa/axon_L))')
h('vSoma.record(&soma.v(0.5))')
h('m.record(&sodiumchan.m)')

# Generate the stimulus with the Ornstein Uhlenbeck process
h.stim = stimulate([1,h.stim, stim_mean, stim_std, h.tau,h.dt,h.T, 1])
h.tstop = h.T
h.run()

va = h.vAIS.to_python()
vs = h.vSoma.to_python()
m = h.m.to_python()

maxva = max(va);
print("Maximum voltage is %f mV"%(maxva))
# Take the axonal voltage with maximum voltage derivative for spike detection voltage.
spthrV = va[np.argmax(np.diff(va)/h.dt)+1] 
print("Spike time threshold is %f mV"%(spthrV))
# Take the axonal voltage 2ms after the spike detection voltage as the reset voltage.
# threshold = va[np.argmax(np.diff(va)/h.dt)+1 + int(2/h.dt)] 
# print("Reset threshold is %f mV"%(threshold))

# Estimate the firing rate and CV of ISI.
a = np.diff((np.array(va)>spthrV)*1.0)
itemindex = np.where(a==1)
sp = np.array(itemindex[0]*h.dt)
fr_estimated = len(sp)/h.T*1000
print("Fr estimated is %f Hz"%(fr_estimated))
isi = np.diff(sp)
CV = np.std(isi)/np.mean(isi)
print("CV is %f"%(CV))

sio.savemat('data_%s_tau%d_posNa%d'%(model, h.tau, h.posNa),{'va':va, 'vs':vs, 'm':m, 'I':h.stim.to_python(),})


