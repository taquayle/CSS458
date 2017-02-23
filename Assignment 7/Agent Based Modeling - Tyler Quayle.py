################################################################################
#   Name: Tyler Quayle
#   Assignment: Agent Based Modeling
#   Date: May 10, 2016
################################################################################
import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt

"""
ATTENTION:
    I tried my damndest on this program. But after 10+ hours i have given up, 
    maybe it's python or a bug in my code. But given 30 frogs at the start, it 
    seems like 20-26 will actually move, and then they will randomly stop moving
    finally all the frog will stop moving. Without a proper debugger i couldn't
    find the source of this issue. No matter the amount of frogs that i start 
    with, the outcome is the same in that they stop 'responding'. I try calling
    Toad.hoppity() after they freeze it doesn't 'respond'. I can still call the
    indivdual variables inside the Toad, just can't use the functions. I was not
    able to any headway into the rest of the program due to trying to solve this
    issue, i know i probably should have restarted, but i kept making little 
    progress steps in debugging it.
    
    Q: What is causing these freezes? the main simulation loop is still running
    but after about 300-600 loops, all frogs stop moving.
    
    There is no excuse for the quality of this turn in, was over confident on 
    the amount of time it would take me to code this.
"""

M = 42                   # grid Length
N = 42                   # grid Width
NUM_OF_DAYS             = 100   # Number of days simulation runs

NUM_DEAD                = 0
NUM_MIGRATED            = 0
TOTAL_FROGS             = 0

AMT_AWP 		= 1.0	# moisture value for water, such as an AWP 
AMT_AWP_ADJACENT 	= 0.4   # moisture value of neighboring cell to water 
AMT_AWP_OVER2 		= 0.2	# moisture value of cell 2 cells away from water 
AMT_DRINK 		= 0.05	# maximum amount toad drinks in 1 time step 
AMT_EAT 		= 0.01	# maximum amount toad eats in 1 time step 
AMT_MIN_INIT 		= 0.88	# minimum initial toad energy and water values 
DESICCATE 		= 0.6  	# level at which desiccation occurs  
FOOD_CELL 		= 0.05  # food value for initializing constant food grid 
FRACTION_WATER 		= 0.6   # fraction of prey that is water 
INIT_PERCENT_TOADS 	= 0.8   # percent chance a StartBorder agent forms a toad 
INIT_RANGE 		= 0.12 	# range of initial toad energy and water values 
MAY_HOP 		= 0.5 	# probability of hopping if not thirsty or hungry 
PERCENT_AWPS 		= 0.01 	# percent chance a grid cell has an AWP
PERCENT_AWPS_FENCED	= 0.6	# percent chance an AWP is fenced 
STARVE 			= 0.6   # level at which starvation occurs 
WATER_HOPPING     	= 0.002 # maximum water used by toad in a hop
ENERGY_HOPPING 		= 0.002	# maximum energy used by toad in a hop 
WOULD_LIKE_DRINK 	= 0.9 	# water level at which toad would like to drink 
WOULD_LIKE_EAT 		= 0.9   # food level at which toad would like to ea

class Toad():
    x = M-1
    y = 0
    hydration = AMT_MIN_INIT
    energy = AMT_MIN_INIT
    dead = False
    migrated = False
    
    def __init__(self, yVal):
        """'
        Initializes toad at Xvalue of M-1 (border) and given Yvalue of yVal,
        with small increase of food+water of INIT_RANGE 
        """
        self.y = yVal
        
        self.energy += np.random.uniform(0, INIT_RANGE)
        self.hydration += np.random.uniform(0, INIT_RANGE)
    
    def eatNdrink(self, grid):
        """
        Eat and Drink on the current tile. The amount the frog can consume is 
        dicated by the AMT_EAT and AMT_DRINK
        """
        if(self.hydration <= WOULD_LIKE_DRINK and grid[self.x, self.y, 1] == 1):
            self.hydration += AMT_DRINK
        if(self.energy <= WOULD_LIKE_EAT and grid[self.x, self.y, 0] >0):
            self.energy += AMT_EAT
            self.hydration += (FRACTION_WATER * AMT_EAT)
            grid[self.x, self.y, 0] -= AMT_EAT
        if(self.hydration > 1):
            self.hydration = 1
    
    def hoppity(self, grid, toadLoc):
        """
        Make a weighted decision on where the toad will jump to, depending on
        it's current energy/hydration. Will priortize water over food. If it 
        doesn't need either. Randomly jump based on MAY_HOP
        """
        if(self.energy < STARVE or self.hydration < DESICCATE):
            self.dead = True
        elif(self.x == 0):
            self.migrated = True
        else:
            tempX = self.x
            tempY = self.y
            bestSpot = 0
            
            moore_x = np.array([-1,0,1,1,1,0,-1,-1]) + self.x
            np.place(moore_x, moore_x >= 41, self.x)
            np.place(moore_x, moore_x < 0, 0)
            moore_y = np.array([-1,-1,-1,0,1,1,1,0]) + self.y
            np.place(moore_y, moore_y >= 41, self.y)
            np.place(moore_y, moore_y < 1, 1)                          
            
            if(self.hydration < WOULD_LIKE_DRINK):    
                for i in range(len(moore_x)):
                    if(grid[(moore_x[i]), (moore_y[i]),1] > bestSpot):
                        bestSpot = grid[(moore_x[i]),moore_y[i],1]
                        tempX = moore_x[i]
                        tempY = moore_y[i]
            
            elif(self.energy < WOULD_LIKE_EAT):
                for i in range(len(moore_x)):
                    if(grid[(moore_x[i]), (moore_y[i]),0] > bestSpot):
                        bestSpot = grid[(moore_x[i]), (moore_y[i]),1]
                        tempX = moore_x[i]
                        tempY = moore_y[i]
            
            elif(ra.rand() < .99):
                hop = ra.randint(0,8)
                tempX = moore_x[hop]
                tempY = moore_y[hop]
                
            if(tempX != self.x and tempY != self.y):
                self.x = tempX
                self.y = tempY
                self.hydration -= WATER_HOPPING
                self.energy -= ENERGY_HOPPING

        

def toadLocations(toads):
    """
    Return a numpy array of all zeros except where the toads are located, which
    become zeros
    """
    tempGrid = np.zeros(shape=(M,N))
    for i in range(len(toads)):
        tempGrid[toads[i].x, toads[i].y] = 1
    return tempGrid

def creategrid(m = 42, n = 42):
    """
    Create and return a numpy array of MxN size, with all values set to the
    FOOD_CELL value
    """
    tGrid = np.zeros(shape=(M,N,2))
    tGrid[:,:,0] = FOOD_CELL
    return tGrid


def createBorder(grid):
    """
    Create the outside border of the desert, with -1 on N,E,S and 2 on W side
    """
    grid[0, :, :] = -1     # Top Row
    grid[-1, :, :] = -1    # Bottom Row
    grid[:, 0, :] = 2   # Left Side
    grid[:, -1, :] = -1  # Right Side
    
def genWater(grid):
    """
    Generates water randomly across the 'map'. Calls createAWP when a point gets
    under the FRACTION_WATER amount
    """
    for i in np.arange(1,M-1):
        for j in np.arange(1,N-1):
            if (ra.random() < PERCENT_AWPS):
                grid[i,j] = createAWP(i,j,grid)

def createAWP(x,y, grid):
    """
    Creates an AWP at the given X,Y. 5x5 border of AMT_AWP_OVER2, 3x3 border of
    AMT_AWP_ADJACENT, middle spot being AMT_AWP
    """
    grid[x-2:x+3, y-2:y+3,1] = AMT_AWP_OVER2 	
    grid[x-1:x+2, y-1:y+2,1] = AMT_AWP_ADJACENT
    grid[x,y,1] = AMT_AWP

def placeToads():
    """
    Place toads on the E Border at a frequency determined by INIT_PERECENT_TOADS
    """
    toadList = []
    for i in np.arange(1,M-1):
        if(ra.random() <= INIT_PERCENT_TOADS):
            toadList.append(Toad(i))
    return toadList

def phaseOne(desert, toads):
    """
    Call Toad.eatNdrink, where toads will consume food/water on their current
    grid spot.
    """
    for t in range(len(toads)):
        curToad = toads[t]
        curToad.eatNdrink(desert)
        
def phaseTwo(desert, toads, curToadLoc):
    """
    Call Toad.hoppity(), which will let the toads 'choose' where to hop to based
    on their current state
    """
    for t in toads:
        t.hoppity(desert, curToadLoc)

def simulate(NUM_OF_DAYS = 1):
    """
    Build the desert size MxN, populate the E border with an amount of frogs
    determined by INIT_PERCENT_TOADS. Then loop thru the steps, each step being
    1 second of a day. Sim length determined by NUM_OF_DAYS. 
    """
    #PHASE 0
    desert = creategrid(M,N)
    genWater(desert)
    createBorder(desert)
    toads = placeToads()
    
    TOTAL = len(toads)
    DEAD = 0
    MIGRATED = 0
    
    plt.ion()
    fig = plt.figure(figsize = (8,5))
    ax = fig.add_axes((0, 0, 1, 1), frameon = False)
    
    visualizer = np.zeros((M,N,3), 'f')
    test =  ax.imshow(visualizer, interpolation = 'none', extent = [0, 42, 0, 42], aspect = 'auto', zorder = 0)
    ax.axis('off')
    
    phaseTwo(desert, toads, toadLocations(toads))
    # Main loop
    for i in range(NUM_OF_DAYS * 3600):


        # CHECK status of toads
        for t in range(len(toads)):
            curToad = toads[t]
            if(curToad.dead == True):
                toads.pop(t)    
                DEAD += 1
                break
            if(curToad.migrated == True):
                toads.pop(t)
                MIGRATED += 1
                break

        phaseOne(desert, toads)
        
        phaseTwo(desert, toads, toadLocations(toads))
        

    ############################################################################
    ########################DISPLAY#############################################

        visualizer = np.zeros((M,N,3), 'f')
        for i in np.arange(0,M-1):
            for j in np.arange(1,N-1):
                visualizer[j,i, 0:1] =  1- desert[i,j,1]
                if(desert[i,j,1] < 1): #NO WATER
                    visualizer[j,i,:] -= desert[i,j,0] * 5
        for i in range(len(toads)):
                visualizer[toads[i].y,toads[i].x,:] = np.array([0,1,0])

        test.set_data(visualizer)
        plt.draw()
        plt.pause(.01)

    return TOTAL, DEAD, MIGRATED

TOTAL_FROGS, NUM_DEAD, NUM_MIGRATED = simulate(NUM_OF_DAYS)

print TOTAL_FROGS, NUM_DEAD, NUM_MIGRATED

