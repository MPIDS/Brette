#!/usr/bin/python
# Calculate the confidence interval of the linear response curve.

import collections, os, time, sys
from subprocess import call

hostname = 'chenfei'
model = 'Brette'
runs = 1000
datafolder = '/dyn_gain/scratch01/%s/%s/'%(hostname, model)
codedirectory = '/home/%s/Code'%(hostname)
outputdirectory = '%s/Output/'%(datafolder)

queue_option = 'qsub -q fulla.q -t 1:%d:1 -b y -j y -cwd -o %s' %(runs, outputdirectory)
programme = '%s/Mechanism/%s/x86_64/special -python' %(codedirectory, model)
script = '%s/transferit/bootstrapping_runme.py'%(codedirectory)
command = queue_option + ' ' + programme + ' ' + script    
call(command, cwd=datafolder, shell=True)


