#!/usr/bin/python
hostname = 'chenfei'
model = 'Brette'  
runs = 1
datafolder = '/dyn_gain/scratch02/%s/%s/'%(hostname, model) 
codedirectory = '/home/%s/Code'%(hostname)
outputdirectory = '%s/Output/'%(datafolder)

import collections, os, time, sys
sys.path.append('%s/scripts'%(codedirectory))
if os.path.isdir(datafolder) == False:
  os.mkdir(datafolder)
  os.mkdir(outputdirectory)

from changeparam import changeparam 
from subprocess import call

IparamTableFile = '%s/Mechanism/%s/IparamTable.txt'%(codedirectory,model) # txt file for stimulus parameters
ParamFile = '%s/scripts/param.hoc'%(codedirectory) # hoc file for neuron parameters

for tau in (5, ): 
    for (thr,posNa) in ((-23,20),): 
      f = 5
      newparams = [('tau',tau),('fr',f),('threshold',thr),('posNa',posNa),('model',model),('codedirectory',codedirectory)]
      changeparam(newparams, IparamTableFile, ParamFile) # Substitute the parameters in param.hoc with those of the current model
      appendix = [s + str(v) for (s,v) in newparams if s != 'model' and s != 'codedirectory']
      foldername = datafolder + ''.join(appendix)
      if os.path.isdir(foldername) == False:
        os.mkdir(foldername)
      bootstrappingdirecotry = foldername+'/bootstrapping/' # make directory for bootstrapping confidence interval
      if os.path.isdir(bootstrappingdirecotry) == False:
        os.mkdir(bootstrappingdirecotry)
      for i in range(1,runs+1):
        call('mkdir -p ' + foldername + '/Series' + str(i) + '/', shell=True)     
      call('cp ' + ParamFile + ' ' + foldername + '/param.hoc', shell=True) # copy param.hoc to the model data directory
      queue_option = 'qsub -q fulla.q -t 1:%d:1 -b y -j y -wd %s -o %s' %(runs, foldername, outputdirectory)
      programme = '%s/Mechanism/%s/x86_64/special -python' %(codedirectory, model)
      script = '%s/scripts/runme.py'%(codedirectory)
      command = queue_option + ' ' + programme + ' ' + script    
      call(command, shell=True) 
   
        
