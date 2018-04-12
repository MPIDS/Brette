# python script for manipulating the parameter file param.hoc

from __future__ import print_function
import re

def changeparam(newparams, IparamTableFile, ParamFile):
  fparam = open(ParamFile,'r')
  params = {}
  # read parameter
  for line in fparam:
    line = line.split('=')
    if len(line) > 1:
      if line[0].strip() == 'model':
        params[line[0].strip()] = line[1].split()[0]
      elif line[0].strip() == 'codedirectory':
        params[line[0].strip()] = line[1].split()[0]
      else:
        params[line[0].strip()] = float(line[1].split()[0])

  fparam.close()
  # change parameter value or add it
  for key, value in newparams:
    params[key] = value

  # read I parameter file
  fItable = open(IparamTableFile,'r')
  labels = fItable.readline().split('\t')  # column labels
  labels[-1] = labels[-1][:-1]  # strip off endline character
  for row in fItable:
    row = row.split('\t')
    correctrow = True
    if len(row)>1:
      for i in range(len(labels)-3):
        correctrow = (float(row[i]) == params[labels[i]]) and correctrow 

      if correctrow:
        params['spthr'] = row[-3]
        params['mean'] = row[-2]
        params['std'] = row[-1][:-1]  # strip off endline character
        break
    else: continue

  fItable.close()

  if not correctrow:
    print('Error: No line in IparamTable mached given parameters!')
    del params['mean']
    del params['std']

  # rewrite the parameter file with new/changes parameters
  fparam = open(ParamFile,'w')
  for key in params.keys():
    if key == 'model':
      print(key + ' = "' + params[key] + '"',file=fparam)
    elif key == 'codedirectory':
      print(key + ' = "' + params[key] + '"',file=fparam)
    else:
      print(key + " = " + str(params[key]),file=fparam)

  fparam.close()
