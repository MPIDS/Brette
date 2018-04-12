#!/usr/bin/python
# Searching for the constant input to reproduce the expected firing rate.

hostname = 'chenfei'
model = 'Brette'
datafolder = '/dyn_gain/scratch02/%s/%s/'%(hostname, model)
codedirectory = '/home/%s/Code'%(hostname)
outputdirectory = '%s/Output/'%(datafolder)

# command for submitting jobs
queue_option = 'qsub -q fulla.q -b y -j y -cwd -o %s' %(outputdirectory)
programme = '%s/Mechanism/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/Parameters/param_step1_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script    

import numpy as np
import time,os
from subprocess import call 
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
if os.path.isdir(outputdirectory) == False:
  os.mkdir(outputdirectory)
rootfolder = datafolder + 'Param/'
if os.path.isdir(rootfolder) == False:
  os.mkdir(rootfolder)

for tau in (5, ): # correlation time
  for (thr, spthr, posNa) in ((-34, -35, 20),): # reset voltage, spike detection voltage, position of the sodium channels 
    for fr in (5,): # firing rate
      leftI = 0.00001 # lowerbound, it is recommended that lower bound not to be zero
      rightI = 0.05 # upperbound, it is recommended that upper bound not to be zero
      precisionFiringOnset = 1e-2 # relative error for parameter searching
      T = 20000 # simulation time, 20s
      param = {}
      param['tau'] = tau
      param['thr'] = thr
      param['spthr'] = spthr
      param['posNa'] = posNa
      param['fr'] = fr
      param['T'] = T  
      param['codedirectory'] = codedirectory   
      param['model'] = model 
      param['leftI'] = leftI
      param['rightI'] = rightI
      param['precisionFiringOnset'] = precisionFiringOnset
      appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
      foldername = rootfolder + appendix
      call('mkdir -p ' + foldername, shell=True) 
      np.save(foldername+'/param', param)
      call(command, cwd=foldername, shell=True) 
      time.sleep(0.1) 



