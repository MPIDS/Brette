#! /usr/bin/python
"""
             InjectStimulus

first argument defines one out of three possible stimulus types:
  0: constant current input
  1: Ornstein-Uhlenbeck process (colored noise)
  2: Sinusoid with additive colored noise
"""
 
def stimulate(li): # isnoisy,mean,std,tau,dt,T,random_seed_index,freq,amp, the last two may not need
  import neuron
  from neuron import h
  isnoisy = li[0]

  if isnoisy == 1:
    m = li[1]
    std = li[2]
    tau = li[3]
    dt = li[4]
    T = li[5]
    seednumber = li[6]
    from random import seed, gauss
    seed(seednumber) # random seed number for generating the same stimulus in runjobs
    from math import exp, sqrt, pi
    x = [m]
    for i in range(int(T/dt)):
      x.append(x[-1] + (1 - exp(-dt/tau)) * (m - x[-1]) + sqrt(1 - exp(-2*dt/tau))*std*gauss(0,1))
    return x


  
