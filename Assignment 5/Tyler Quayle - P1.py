################################################################################
#   Name: Tyler Quayle
#   Assignment: Monte Carlo 2, Problem 1
#   Date: April 26, 2016
################################################################################

import random as ra
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

def SAW(num = 100, grid_size = 12):
    """
    Call oneSAW num of times, putting all results into moveList and returning it.
    Returns. [List][x[],y[],steps]
    """
    moveList = []
    for i in range(num):
        moveList.append(oneSAW(grid_size))
    return moveList
        
def oneSAW(grid_size):
    """
    Generate 1 Self avoiding walk, returning 2 lists, 1 for all X coordinates
    1 for all Y coordinates and 1 variable indicating the number of steps taken
    """
    move = [(1.,1.), (-1.,1.), (-1.,-1.), (1., -1.)] #possible moves
    grid_size+=1
    steps = 1
    curX = grid_size//2
    curY = grid_size//2
    x=[curX]
    y=[curY]
    grid = np.arange(grid_size**2).reshape(grid_size,grid_size)
    grid[:] = 0
    grid[curX][curY] = 1
    while True:
        dx, dy = ra.choice(move)
        curX += dx
        curY += dy
        if(curX >= grid_size or curY >= grid_size # Hitting Boundries
            or curX < 0 or curY < 0):
            curX -= dx
            curY -= dy
        else:
            if(grid[curX][curY] == 0):
                x.append(curX-(grid_size/2))
                y.append(curY-(grid_size/2))
                steps += 1
                grid[curX][curY] = steps
            else:
                break
    x[0] = 0
    y[0] = 0
    return x,y, steps

def fracList(n_tests, maxstep, step_list):
    """
    Return a list containing the amount of times a certain number of steps
    occurs.
    """
    fractions = np.bincount(step_list)
    fractions = fractions/float(n_tests)
    return fractions

def RN(SAWList, maxstep):
    """
    Calculate the Root-Mean-Square of 'n' steps.
    Return as a list
    """
    rn = np.zeros(maxstep+1)
    steps = SAWList[:,2]
    for i in range(len(SAWList)):
        rn[steps[i]] += (SAWList[i][0][-1]**2 + SAWList[i][1][-1]**2)
    rMask = ma.masked_array(rn, 0)
    oMask = ma.masked_array(np.bincount(steps.astype(int)),0)+1
    rMask = np.sqrt(rMask/oMask)
    return rMask

if __name__ == "__main__":   #IF Run from cmd line will execute this
#==============================================================================
# USER ADJUSTABLE    
    GRID_SIZE = 22
    N_TESTS = 100000
    MIN_COND = 20
#==============================================================================  

    SAWList = np.array(SAW(N_TESTS,GRID_SIZE)) #Returns 4-d array
    x = SAWList[:,0] 
    y = SAWList[:,1]
    steps = SAWList[:,2]
    index_max = steps.argmax()
    
    fList = fracList(N_TESTS, max(steps), steps.astype(int)) 
    rList = RN(SAWList, max(steps))
    plt.ion()

#------ PLOT SELF AVOIDING WALK -------
    plt.title('Self Avoiding Walk')
    plt.xlabel('Max Steps: '+ str(max(steps)) + ' Tests: ' +
            str(N_TESTS) + ' Grid Size: '+ str(GRID_SIZE)+'x'+str(GRID_SIZE))
    plt.xlim(-GRID_SIZE//2,GRID_SIZE//2)
    plt.ylim(-GRID_SIZE//2,GRID_SIZE//2)
    l = plt.axvline(x=0)
    l = plt.axhline(y=0)
    for i in range(len(x[index_max])): #Step by Step longest polymer
        plt.plot(x[index_max][:i], y[index_max][:i], 'r')
        plt.pause(.1)
#------ PLOT PERCENTAGE OF OCCURENCES -----    
    plt.figure()
    plt.plot(fList[2:])
    plt.title('f(n)')
    plt.ylabel('Percentage of occurance')
    plt.xlabel('Polymer Length, Max Length: ' + str(max(steps)))
#------ PLOT DISPLACEMENT -----    
    plt.figure()
    plt.plot(rList)
    plt.title('Rn: Root-Mean-Square')
    plt.ylabel('Displacement')
    plt.xlabel('Polymer Length, Max Length: ' + str(max(steps)))
    plt.xlim(2, max(steps))
    plt.show()