#! /usr/bin/python
# For a given mean of the stimulus, search for the std of the stimulus to reproduce 5Hz firing rate.

hostname = 'chenfei'
model = 'Brette'
datafolder = '/dyn_gain/scratch02/%s/%s/'%(hostname, model)
codedirectory = '/home/%s/Code'%(hostname)
outputdirectory = '%s/Output/'%(datafolder)

runs = 200
queue_option = 'qsub -q fulla.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Mechanism/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/Parameters/param_step2_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script  


import time
from subprocess import call
import numpy as np

for tau in (5,50): # 5,
    for (spthr,posNa) in ((-35, 20),): 
      fr = 5
      appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
      foldername = datafolder + 'Param/' + appendix  
      for i in range(1,runs+1):
        call('mkdir -p ' + foldername + '/mean'+str(i), shell=True)
      call(command, cwd=foldername, shell=True)  
