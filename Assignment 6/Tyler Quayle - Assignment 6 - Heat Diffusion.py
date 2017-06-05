################################################################################
#   Name: Tyler Quayle
#   Assignment: Cellular Automaton Simulations, Problem 1
#   Date: May 3, 2016
################################################################################

import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt

def diffusion(rate, site, N, NE, E, SE, S, SW, W, NW):
    """
    Returns the sites updated temp, based on surronding moore cells
    """ 
    return (1-(8*rate))*site + rate*(N+NE+E+SE+S+SW+W+NE)

def createGrid(xMax, yMax, cold, ambient, hot):
    """
    Create grid of XxY size, setting the outside cells to be 0. Every cell set 
    to ambient temp, with 2 section of cells given cold or hot values 
    """
    grid = np.zeros((xMax*yMax), dtype='f').reshape(yMax,xMax)
    grid[:] = ambient
    #grid[0] = 0     # Top Row
    #grid[-1] = 0    # Bottom Row
    #grid[:,0] = 0   # Left Side
    #grid[:,-1] = 0  # Right Side
    grid[-2,3:9] = hot
    grid[2:6,1] = cold
    return grid

def NS(xMax, yMax, n_times, rate, cold, ambient, hot):
    """
    Run the diffusion simulation n_times steps, return the results. Using the 
    equation provided in the book.
    site + ∆site = (1 – 8r)site + r (i=1,8)∑  8 neighbor, where 0 < r < 0.125 
    """
    tGrid = createGrid(xMax, yMax, cold, ambient, hot)
    stepGrid = np.array(tGrid)
    
    for n in range(n_times):
        for i in np.arange(1, yMax-1):
            for j in np.arange(1, xMax-1):
                stepGrid[i][j] = diffusion(rate, tGrid[i][j], 
                                tGrid[i-1][j], tGrid[i-1][j+1], #N, NE
                                tGrid[i][j+1], tGrid[i+1][j+1], #E, SE
                                tGrid[i+1][j], tGrid[i+1][j-1], #S, SW
                                tGrid[i][j-1], tGrid[i-1][j-1]) #W, NW
        tGrid = np.array(stepGrid)
    return tGrid

def stocDiffusion(xMax, yMax, n_times, rate, cold, ambient, hot):
    """
    Run the Stochastic diffusion simulation for n_time steps. 
    Where the equation is not static, but instead has a small flucuations in 
    each cell. ranDiff holds each steps random number. So that sum(ranDiff)==1
    """
    ranDiff = ra.normal(0,.5, size=(8,))
    ranDiff += ((0.0 - np.sum(ranDiff))/8.0)
    tGrid = createGrid(xMax, yMax, cold, ambient, hot)
    stepGrid = np.array(tGrid)
    
    for n in range(n_times):
        for i in np.arange(1, yMax-1):
            for j in np.arange(1, xMax-1):
                stepGrid[i][j] = \
                (((1.0-(rate*(8.0 + np.sum(ranDiff)))) * tGrid[i,j]) +
                    (rate * (1.0+ranDiff[0]) * tGrid[i-1][j])+              #N
                    (rate * (1.0+ranDiff[1]) * tGrid[i-1][j+1])+            #NE
                    (rate * (1.0+ranDiff[2]) * tGrid[i][j+1])+              #E
                    (rate * (1.0+ranDiff[3]) * tGrid[i+1][j+1])+            #SE
                    (rate * (1.0+ranDiff[4]) * tGrid[i+1][j])+              #S
                    (rate * (1.0+ranDiff[5]) * tGrid[i+1][j-1])+            #SW
                    (rate * (1.0+ranDiff[6]) * tGrid[i][j-1])+              #W
                    (rate * (1.0+ranDiff[7]) * tGrid[i-1][j-1]))            #NW
        tGrid = np.array(stepGrid)
    return tGrid

    

################################USER CHANGEABLE#################################
gridX = 30
gridY = 10
difRate = .1
nTimes = 20
cold = 0
ambient = 25
hot = 50       
################################################################################                     

#   GET NON-STOCHASTIC GRID
NSGrid = NS(gridX,gridY,nTimes,difRate, cold, ambient, hot)
#   GET STOCHASTIC GRID
SGrid = stocDiffusion(gridX,gridY,nTimes,difRate, cold, ambient, hot)


#######################PLOT Non-Stochastic######################################
fig = plt.figure(figsize=(gridX/2,gridY/2))
ax = fig.add_axes((0,0,1,1))
ax.set_title('Non Stochastic')
img = ax.imshow(NSGrid, interpolation='none', cmap=plt.cm.RdBu_r,
                    extent=[0,gridX,0,gridY], aspect = 'auto', zorder=0)

#######################PLOT Stochastic##########################################
fig = plt.figure(figsize=(gridX/2,gridY/2))
ax = fig.add_axes((0,0,1,1))
img = ax.imshow(SGrid, interpolation='none', cmap=plt.cm.RdBu_r,
                    extent=[0,gridX,0,gridY], aspect = 'auto', zorder=0)

plt.show()
