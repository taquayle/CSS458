################################################################################
# NAME:          Tyler Quayle                                                  #
# ASSIGNMENT:    1                                                             #
# PART:          Distance                                                      #
################################################################################

import numpy as N        #Numpy Module, used to create the arrays
import math as M         #Math Module, used for the Power and Sq Root functions 

# distance(x,y,pt)
# Given a set of X,Y coordinates, return a matrix (dist) showing distance of 
# each point (x,y) to point pt. Distance = SQRT((X - pt.X)^2 + (Y - py.Y)^2)
def distance(x, y, pt):   
    dist = N.zeros((N.size(y),N.size(x))) #Create correct matrix size
    for i in x:
        for j in y:
            dist[j][i] = M.sqrt((M.pow((x[i]-pt[0]),2))+(M.pow((y[j]-pt[1]),2)))
    return dist   
    

################################################################################
# Execute
if __name__ == "__main__":   
    x = N.arange(5)
    y = N.arange(4)
    print(distance(x,y,[-2.3,3.3]))