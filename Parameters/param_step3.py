#! /usr/bin/python
# Summarize the mean-std and mean-CV relation. Find the mean and std that reproduce expected firing rate and CV by hand.

hostname = 'chenfei'
model = 'Brette'
datafolder = '/dyn_gain/scratch01/%s/%s/'%(hostname, model)
codedirectory = '/home/%s/Code'%(hostname)
outputdirectory = '%s/Output/'%(datafolder)

runs = 200
import numpy as np
import scipy.io as sio
import os.path
for tau in (5,): 
    for (spthr,posNa) in ((-35, 20),):
        fr = 5
        appendix = 'tau%dfr%dspthr%dposNa%d'%(tau, fr, spthr, posNa)
        foldername = datafolder + 'Param/' + appendix  
        data = np.load(foldername + '/param.npy')
        param = data.item()
        thr = param['thr']
        mean =  []
        std = []
        cv = []
        for i in range(1,runs+1):
            if os.path.isfile(foldername+'/mean%d/std_mean_cv.npy'%(i)) == True:
              data = np.load(foldername+'/mean%d/std_mean_cv.npy'%(i))
              dic = data.item()
              mean.append(dic['mean'])
              std.append(dic['std'])
              cv.append(dic['cv'])
            else: continue

        sio.savemat(foldername+'_mean_std_cv',{'mean':mean, 'std':std, 'cv':cv, 'thr':thr})
