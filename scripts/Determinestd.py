#! /usr/nld/python
"""
             Searching for the std to reproduce the expected firing rate.

The searching algorithm is the same as that in file firingoset
"""

def DetermineStdI(leftStd, rightStd, precision_std, apc, mean, stim, tau, dt,T, fr_set,seednumber):
  import neuron
  from neuron import h
  from I_proc import stimulate
  while ((rightStd-leftStd) > precision_std*max([abs(rightStd), abs(leftStd)])):
    if leftStd == 0 and rightStd<1e-7:
      break
      return rightStd
    print("leftStd is %f, rightStd is %f"%(leftStd, rightStd))
    print("rightStd-leftStd: %f , precision_std: %f \n" %((rightStd-leftStd), precision_std))
    h.finitialize()
    h.fcurrent()
    h.frecord_init()
    apc.n = 0 
    std = (leftStd+rightStd)/2
    print('std for test is %f'%(std))
    h.stim = stimulate([1,stim,mean,std,tau,dt,T,seednumber]) 
    h.tstop = T 
    h.run()
    fr = apc.n/float(T/1000)
    print('fr is %f'%(fr))
    if (fr <= fr_set): 
      leftStd = std
    else:
      rightStd = std

  return std
