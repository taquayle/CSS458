################################################################################
#   Name: Tyler Quayle
#   Assignment: Computational Error
#   Date: April 12, 2016
################################################################################
"""
Build a model to compute a continous growth of 9.3% on a starting value of $500
over 10, 20, 30, and 40 years. Then compare the computed values to the answers
given by analytical means. Find absolute and relative differences between them.

"""

import numpy as np
import matplotlib.pyplot as plt

growth_rate = .093     #%
starting_cash = 500    #$

start = 0              #Years
end = [10.,20.,30.,40.]    #Years

times_daily = 1
deltaT = 1./(365.*times_daily)

time = []       # An array, contains each of the time arrays
result = []     # An array, containing all computed data
analytical = [] # An array of all the answered done analytical

tempData = []   
tempData.append(starting_cash)

x = np.arange(start, end[-1], deltaT)

# Compute the analytical answer
analytical.append(starting_cash*(np.exp((end[-1]*growth_rate))))

for j in range(1, len(x)):
    # Append the new value into tempData
    tempData.append(tempData[j-1]+(growth_rate*tempData[j-1]*deltaT))

    
analytical_find_amounts = np.in1d(x, end)  
#analytical_find_amounts = tempData[np.where(np.in1d(x, end))]
#analytical_find_times = x[analytical_find_amounts]
    
    
