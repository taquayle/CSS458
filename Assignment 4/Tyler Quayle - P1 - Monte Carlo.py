################################################################################
#   Name: Tyler Quayle
#   Assignment: Monte Carlo, Problem 1
#   Date: April 18, 2016
################################################################################
import math as ma
import random as ra
import numpy as np
import matplotlib.pyplot as plt


def FoX(x):
    """Function representing F(x)=sqrt(cos^2(x)+1)"""
    return ma.sqrt(ma.cos(x)**2+1)

def DART():
    """Function to simulate throwing a dart"""
    coord = []
    coord.append(ra.uniform(0,2.0))
    coord.append(ra.uniform(0,1.5))
    return coord
    
num_of_attempts = 60
starting_darts = 10
ending_darts = 1000
steps = ending_darts/10

darts_thrown = np.arange(starting_darts,ending_darts, steps)
results = np.zeros(shape=[len(darts_thrown),num_of_attempts])

for i in range(0, len(darts_thrown)):
    for j in range(0,num_of_attempts):
        hit = 0.
        for k in range(0, darts_thrown[i]):
            throw = DART()
            if(throw[1] < FoX(throw[0])):
                hit+=1
        results[i][j]=(hit/darts_thrown[i])

stdDev = []
for i in range(0,len(darts_thrown)):
    mean = np.mean(results[i])
    for j in range(0,num_of_attempts):
        results[i][j] -= mean
        results[i][j] = results[i][j]**2
    mean = np.mean(results[i])
    stdDev.append(np.sqrt(mean))     

plt.plot(stdDev)
plt.title("Standard Deviation v Darts Thrown")
plt.ylabel("Standard Deviation")
plt.xlabel("Number of Darts Thrown (x100)")
plt.show()