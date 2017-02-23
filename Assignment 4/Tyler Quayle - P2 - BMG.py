################################################################################
#   Name: Tyler Quayle
#   Assignment: Monte Carlo, Problem 2
#   Date: April 18, 2016
################################################################################
import math as ma
import random as ra
import numpy as np
import matplotlib.pyplot as plt

def BMG(size, mean=9, stdDev=2):
    """ Function to return a list of coordinates created using the 
    Box-Muller-Gauss method, number of items in list being SIZE. Mean and
    stdDev default to 9 and 2 respectively"""
    x = []
    y = []
    result_list = []
    for i in range(0,size):
        a = ra.uniform(0., 2*ma.pi)
        b = stdDev*ma.sqrt(-2*np.log(ra.uniform(0.,1.)))
        x.append(b*ma.sin(a)+mean)
        y.append(b*ma.cos(a)+mean)
    result_list.append(x)
    result_list.append(y)
    return result_list        

bmg_list = BMG(500)
tblGauss = sum(bmg_list, [])

plt.hist(tblGauss)
plt.title("Histogram of Box-Muller-Gauss")
plt.ylabel("Times Returned")
plt.xlabel("Number Returned")
plt.show()