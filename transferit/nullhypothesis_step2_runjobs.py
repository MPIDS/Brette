#!/usr/bin/python
# Take the shuffled STA in each Series folder, calculate the linear response curve for null hypothesis test
import collections, os, time, sys
from subprocess import call

hostname = 'chenfei'
model = 'Brette'
runs = 500 # null hypothesis runs
datafolder = '/dyn_gain/scratch02/%s/%s/'%(hostname, model)
codedirectory = '/home/%s/Code'%(hostname)
outputdirectory = '%s/Output/'%(datafolder)

queue_option = 'qsub -q fulla.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Mechanism/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/transferit/nullhypothesis_step2_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script 

for tau in (5,): 
    for (thr,posNa) in ((-23,20),): 
      f = 5 
      appendix = 'tau%dfr%dthreshold%dposNa%d'%(tau, f, thr, posNa)
      foldername = datafolder + appendix
      if os.path.isdir(foldername+'/nullhypothesis') == False:
        os.mkdir(foldername+'/nullhypothesis')
      call(command, cwd=foldername, shell=True)

