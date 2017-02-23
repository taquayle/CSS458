################################################################################
#   Name: Tyler Quayle
#   Assignment: Cellular Automaton Simulations, Problem 2
#   Date: May 3, 2016
################################################################################

import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt
import matplotlib.colors as col

def createForest(n):
    """
    Creates a forest of (n x n) size. Also creates border cells set to 2, which
    are ignored by the simulation.
    
     RETURN
     ------
     grid - n x n inside of (n+2 x n+2) grid of 0 (tree) and -1 (burning) 
            at center.  
    """
    grid = np.zeros((n+2)**2).reshape(n+2,n+2)
    grid[n/2][n/2] = -1
    grid[0] = 2     # Top Row
    grid[-1] = 2    # Bottom Row
    grid[:,0] = 2   # Left Side
    grid[:,-1] = 2  # Right Side
    return grid

def burnCheck(p, tree):
    """
    Checks to see if tree exists (0) and then 'rolls' a random number between 0 
    1, if that number is smaller then p(probability) then tree catches fire (-1)
    else, return whatever the current state of the tree is
    
    RETURN
    ------
    -1 - If tree exists and random < probability
    tree - Returns trees current state if random > probability or tree burnt
    """
    if(tree == 0 and ra.random() < p):
        return -1
    return tree
      
def burnStep(p, n, forest):
    """
    Simulate 1 step of the forest fire, creating a temp array that will get the
    results from 1 step. Must use temp or fire will 'spread' in the direction
    of for loops (higher index) on successive checks
    
    RETURN
    ------
    temp - 1 simulated step of the forest fire
    """
    temp = np.array(forest)
    for i in np.arange(1,n+1):
        for j in np.arange(1,n+1):
            if (forest[i][j] == -1): # fire
                temp[i-1][j] = burnCheck(p, forest[i-1][j])
                temp[i][j+1] = burnCheck(p, forest[i][j+1])
                temp[i+1][j] = burnCheck(p, forest[i+1][j])
                temp[i][j-1] = burnCheck(p, forest[i][j-1])
                temp[i][j] = 1 #TreeGone
    return temp

def burnDown(p, n, steps):
    """
    Simulate a forest burning for [steps] amount of time, create list where each
    index simulates 1 step of the forest fire
    
    RETURN
    ------
    simulation - List of Numpy arrays indicating each step of the forest fire
    """
    forest = createForest(n)
    simulation = [forest]
    
    for i in range(steps):
        forest = np.array(burnStep(p,n,forest))
        simulation.append(forest)
    return simulation

################################################################################
steps = 20
n = 17
p = np.arange(.1,1,.1)
################################################################################
data = np.zeros(90).reshape(9,10)
sim = 0

for i in range(len(p)):
    for j in range(10):
        sim = burnDown(p[i], n, steps)
        data[i][j] =  (np.sum(sim[-1])-144)/(n**2)
     
burnPercent = np.zeros(len(p))
for i in np.arange(0,9):
    burnPercent[i] = np.average(data[i])


####################ANIMATE BURN SEQUENCE ######################################
plt.ion()
fig = plt.figure(figsize=(n/2,n/2))
ax = fig.add_axes((0,0,1,1))

earth = '#654321'
fire = '#FF6600'
forest_color = col.ListedColormap([fire, 'green', earth, 'black'])
 
for i in range(steps-1):
    img = ax.imshow(sim[i], cmap= forest_color, interpolation='none')
    plt.pause(.1)

####################PLOT PERCENTAGES VS PROBABILITY#############################
plt.figure()
plt.plot(p, burnPercent)
plt.xlim(.1,.9)
plt.title('Burn % V. Burn Probability')
plt.xlabel('Probability')
plt.ylabel('% Burned')
plt.show()