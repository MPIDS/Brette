#! /usr/bin/python
"""
             InjectStimulus

first argument defines one out of three possible stimulus types:
  0: constant current input
  1: Ornstein-Uhlenbeck process (colored noise)
  2: Sinusoid with additive colored noise
"""
 
def stimulate(li): # isnoisy,h.stim,mean,std,tau,dt,T,random_seed_index,freq,amp, the last two may not needed
  import neuron
  from neuron import h
  isnoisy = li[0]
  stim = li[1]
  if isnoisy == 0:
    stim.resize(1)
    stim.x[0] = li[2]

  if isnoisy == 1:
    m = li[2]
    std = li[3]
    tau = li[4]
    dt = li[5]
    T = li[6]
    seednumber = li[7]
    from random import seed, gauss
    seed(seednumber)
    from math import exp, sqrt, pi
    x = [m]
    for i in range(int(T/dt)):
      x.append(x[-1] + (1 - exp(-dt/tau)) * (m - x[-1]) + sqrt(1 - exp(-2*dt/tau))*std*gauss(0,1))
    stim.from_python(x)

  if isnoisy == 2:
    m = li[2]
    std = li[3]
    tau = li[4]
    freq = li[-2]
    amp = li[-1]
    dt = li[5]
    T = li[6]
    seednumber = li[7]
    from random import seed, gauss
    seed(seednumber)
    from math import exp, sqrt, sin, pi
    x = [m]
    for i in range(int(T/dt)):
      x.append(x[-1] + (1 - exp(-dt/tau)) * (m - x[-1]) + sqrt(1 - exp(-2*dt/tau))*std*gauss(0,1))

    for i in range(int(T/dt)):
      x[i] = x[i] + amp*sin(2*pi*freq*i*dt/1000)

    stim.from_python(x)

  return stim


  
