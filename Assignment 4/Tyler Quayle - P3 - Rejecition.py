################################################################################
#   Name: Tyler Quayle
#   Assignment: Monte Carlo, Problem 3
#   Date: April 18, 2016
################################################################################
import numpy as np
import math as ma
import matplotlib.pyplot as plt
import random as ra

def rej():
    """ Function rej, uses the rejection method to return a rand number within
    the bounds of the function F of X (FoX). Recursively calls itself until
    FoX(rand) is greater than a random number generated from 0 to 2pi"""
    rand = ra.uniform(0.0, 0.25)
    if(FoX(rand) > ra.uniform(0.0, 2*ma.pi)):
        return rand
    else:
        return rej()

def FoX(x):
    """Function F of X, used to simulate f(x) = 2pi*sin(4*pi*x)"""
    return 2*ma.pi*ma.sin(4*ma.pi*x)

func_plot = []
rej_plot = []
for i in np.arange(0,.26, .01):
    func_plot.append(FoX(i))

for i in range(0,1000):
    rej_plot.append(rej())

plt.hist(rej_plot)
plt.title("Histogram for Rejection Method")
plt.ylabel("Times Returned")
plt.xlabel("Number Returned")
plt.show()