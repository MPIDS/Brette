#!/usr/bin/python
# Calculate the null hypothesis test curve
# Step1, in each Series folder,  generate 500 pieces of STA with the shuffled spike time 
import collections, os, time, sys
from subprocess import call

hostname = 'chenfei'
model = 'Brette'
runs = 400 # series numbers in runjob
datafolder = '/dyn_gain/scratch02/%s/%s/'%(hostname, model)
codedirectory = '/home/%s/Code'%(hostname)
outputdirectory = '%s/Output/'%(datafolder)

queue_option = 'qsub -q fulla.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Mechanism/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/transferit/nullhypothesis_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script  
 
for tau in (5,): 
    for (thr,posNa) in ((-23,20),): 
      f = 5 
      appendix = 'tau%dfr%dthreshold%dposNa%d'%(tau, f, thr, posNa)
      foldername = datafolder + appendix
      call(command, cwd=foldername , shell=True)    
