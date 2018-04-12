# Brette
Model simulation and linear response function calculation

To run the simulation, we used NEURON 7.3 with Python 2.6. 

1. Compile the neuron model:

    a. Go to the directory ~/Code/Mechanism/Brette. Compile the mod files with nrnivmodl.

2. Searching for the parameters of the stimulus for simulation 
a. Determine the axonal voltage with the maximum votlage derivative as spike detection voltage. In param_step0.py, set thresold to 60mV. Injecting the neuron model with a constant input, one can determine the spike detection voltage. To run this file: ~/Code/Mechanism/Brette/x86_64/special -python param_step0.py
b. Temporarily taking the voltage slightly larger than the spike detection voltage as the reset voltage, search for the constant input to generate 5Hz firing rate in the neuron model with the files param_step1_runjobs.py and param_step1_runme.py. Under the constant input for 5Hz firing rate, take the axonal voltage 2ms after the spike detection voltage as the reset voltage.
c. For a given mean of the stimulus, search for the std of the stimulus to reproduce 5Hz firing rate with param_step2_runjobs.py and param_step2_runme.py.
d. Summarize the mean-std and mean-CV relation with param_step3.py. Find the mean and std that reproduce expected firing rate and CV by hand.

3. Calculate the linear response curves.
a. Write the simulation parameters in the file IparamTable.txt in ~/Code/Mechanism/Brette.
b. Calculate the STA for linear response curves with the file runjobs.py in ~/Code/runjobs.
c. Calculate the linear response curves with the file transferit.py in ~/Code/transferit. To run this file: ~/Code/Mechanism/Brette/x86_64/special -python transferit.py

4. Bootstrapping confidence interval and null hypothesis test.
a. Calculate the bootstrapping confidence interval with bootstrapping_runjobs.py. Write the upper bound and lower bound of the confidence intervals into the file of linear response curve with bootstrapping_step2.py.
b. Calculate the STA with the shuffled spike times with null_hypothesis_runjobs.py. Use these STAs to calculate the linear response curve with nullhypothesis_step2_runjobs.py. Take the 95 percent bound of these curves as the null hypothesis test curve with nullhypothesis_step3.py.

To calculate the linear response curves of Brette's model with high voltage sensitivity, change the sodium activation parameter k_{a} from 6mV to 0.1mV in NaBrette_point.mod and Neuron.hoc, then compile the mod files. For the neuron model with a small soma, change the soma length and diameter from 50um to 10um in Neuron.hoc.
