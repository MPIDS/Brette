#! /usr/nld/python
"""
             Searching for the constant input to reproduce the expected firing rate.

1. Set the upper bound and lower bound of the target parameter by hand.
2. Estimate the firing rate generated with the mean of the upper bound and the lower bound.
3. If the firing rate is too small, we will replace lowerbound with middle point. If the firing rate is too large, we will replace upperbound with middle point.
4. The searching iteration will stop when the difference between the upper bound and the lower bound is smaller than 1% of the magnitude of the upper bound or the lower bound. Here the percision parameter 1% is set by hand.
5. If the expected firing rate is larger than 0, it will return the upper bound. If the expected firing rate is 0, it will return the lower bound. 
"""

def FiringOnset(leftI, rightI, precision, apc, stim, T, fr_set): 
  import neuron
  from neuron import h
  from I_proc import stimulate 
  while ((rightI-leftI) > precision*max([abs(rightI), abs(leftI)])):
    print("leftI is %f, rightI is %f"%(leftI, rightI))
    print("rightI-leftI: %f , precision: %f \n" %((rightI-leftI), precision))
    h.finitialize()
    h.fcurrent()
    h.frecord_init()
    apc.n = 0 
    mean = (leftI+rightI)/2
    print('mean is %f'%(mean))
    h.stim = stimulate([0,stim,mean]) 
    h.tstop = T 
    h.run()
    fr = apc.n/float(T/1000) 
    print('fr is %f'%(fr))
    if (fr <= fr_set): 
      leftI = mean # If the firing rate is too small, we will replace lowerbound with middle point
    else:
      rightI = mean # If the firing rate is too large, we will replace upperbound with middle point
  
  if fr_set>0: 
    return rightI
  else:
    return leftI

