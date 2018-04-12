#! /usr/bin/python
import os, neuron, sys
from neuron import h
import numpy as np
from sys import argv

os.environ.keys()
i = int(os.environ['SGE_TASK_ID']) # index of the job number
print('i = %d'%(i))

h('strdef model, codedirectory')
h('load_file("param.hoc")') 
sys.path.append('%s/scripts'%(h.codedirectory))
paramstr = []
h('load_file("nrngui.hoc")')
fullpath = os.getcwd()
fullpath = fullpath + '/Series' + str(i) + '/'
tmp_str = '%s/Mechanism/%s/Neuron.hoc'%(h.codedirectory, h.model)
h.load_file(tmp_str)
from I_proc import stimulate

h.dt = 0.025 # time step (ms)
spiketimelist = [] # the list of spike times for 50 repetitions of 20s simulation
N = int(h.T/h.dt)    
dt = h.dt*10**-3 # time step (s)
T = N*dt # 20s
sf = 1/dt # sampling frequency, sf = 40000Hz
maxtau = int(0.4*sf) 
L = maxtau*2 # length of the STA, 0.8s, L=32000

nspikes = 0 # the total number of spikes
STA_tmp = np.zeros(L) # the sum of all spike triggered stimuli

h('access soma')
h.T = h.T + h.T_relax # 20s of simulation time and 0.5s of randomization of initial condition 
h('objref APgen, stimulus, stim, vAIS')
h('axon APgen = new NetCon(&v(posNa/axon_L), sodiumchan,threshold,0,0)')
h('axon {sodiumchan.loc(posNa/axon_L)}')

h.stimulus = h.IClamp(0.5)
h.stimulus.dur = 1e9
h.stimulus.delay = 0
h.stimulus.amp = 0
h.stim = h.Vector()
h('stim.play(&stimulus.amp, dt)')

paramstr.append('T=%f'%(h.T-h.T_relax))
paramstr.append('dt=%f'%(h.dt))
paramstr.append('posNa=%f'%(h.posNa))
paramstr.append('threshold=%f'%(h.threshold))
paramstr.append('fr=%f'%(h.fr))
paramstr.append('rep=%f'%(h.rep))
paramstr.append('isnoisy=%d'%(1))
paramstr.append('stochastic_process=%s'%('"Ornstein-Uhlenbeck process statistics"'))
paramstr.append('mean=%f'%(h.mean))
paramstr.append('std=%f'%(h.std))
paramstr.append('tau=%f'%(h.tau))

np.save(fullpath+'/param', paramstr)
print('mean=%f, std=%f, tau=%f\n' %(h.mean,h.std,h.tau))
print('\nAll is set: SIMULATION START!\n\n')

for k in range(int(h.rep)): 
  print('Loop at %d\n' %(k))
  seednumber = i*100+k # i is Series number, k is repitition number k = 0, 1, ..., 49
  h.stim.resize(0)
  h('stim.play(&stimulus.amp, dt)') 
  h.finitialize()
  h.frecord_init()
  h.vAIS = h.Vector(int(h.T/h.dt))  
  h('vAIS.record(&axon.v(posNa/axon_L))') 
  h.stim = stimulate([1,h.stim,h.mean,h.std,h.tau,h.dt,h.T, seednumber])
  h.tstop = h.T
  h.run()
  va = h.vAIS.to_python() 
  a = np.diff((np.array(va)>h.spthr)*1.0)
  itemindex = np.where(a==1) 
  sp1 = np.array(itemindex[0]*h.dt) # spike times in 20.5s.
  sp2 = (sp1[sp1>500] - 500)/1000.0 # rule out the spike in first 500ms, and deduct the randomization time
  spiketimelist.append(sp2)  
  skipspikeslist = sum(sp2<(maxtau+1)*dt) # to find the spikes having complete 0.8s in 20s simulatio time, skip the spikes in the first 0.4s.
  idxlist = skipspikeslist
  stim = h.stim.to_python()
  stim = stim[int(500/h.dt):] # deduct the stimulus in the randomization time, 500ms
  while (len(sp2) > idxlist):
    if (sp2[idxlist]/dt + maxtau < N): # if there is still 0.4s simulation time after the spike time.
      STA_tmp_add =  stim[(int(sp2[idxlist]/dt)-maxtau-1):(int(sp2[idxlist]/dt)+maxtau-1)] # spike triggered stimulus
      STA_tmp = STA_tmp + np.array(STA_tmp_add)
      idxlist = idxlist + 1
    else: break
  nspikes = nspikes + idxlist - skipspikeslist  

STA = STA_tmp/float(nspikes) - h.mean
np.save(fullpath+'/STA', {'STA':STA})
np.save(fullpath+'/spiketimelist', {'spiketimelist':spiketimelist})
