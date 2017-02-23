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
end = [10,20,30,40]    #Years

times_daily = 1
deltaT = 1./(365.*times_daily)

time = []       # An array, contains each of the time arrays
result = []     # An array, containing all computed data
analytical = [] # An array of all the answered done analytical

modelDouble = 0.
analyticalDouble = np.log(2)/growth_rate
modelQuad = 0.
analyticalQuad = np.log(4)/growth_rate

for i in range(0, len(end)):
    # Create temp array for this step in years
    tempData = []   
    tempData.append(starting_cash)
    
    x = np.arange(start, end[i], deltaT)
    time.append(x)
    
    # Compute the analytical answer
    analytical.append(starting_cash*(np.exp((end[i]*growth_rate))))
    
    for j in range(1, len(x)):
        # Append the new value into tempData
        tempData.append(tempData[j-1]+(growth_rate*tempData[j-1]*deltaT))
        
        # Find double and quad time using the model
        if(modelDouble == 0):
            if(np.allclose(1000., tempData[j],1e-4, 1e-4)):
                modelDouble = x[j]
        if(modelQuad == 0):
            if(np.allclose(2000., tempData[j],1e-3, 1e-3)):
                modelQuad = x[j]
    #Add the temp data into result, result contains all lists of data from
    #each interatin (10yrs, 20yrs, 30yrs, etc)
    result.append(tempData)

print 'Model Time to Double:     ', modelDouble
print 'Analytical Time to Double:',analyticalDouble
print '\tAbsoulute Error:', np.abs(modelDouble-analyticalDouble)
print '\tRelative  Error:', (np.abs(analyticalDouble-modelDouble)
                                /analyticalDouble)*100
print '\nModel Time to Quadruple:     ', modelQuad
print 'Analytical Time to Quadruple:', analyticalQuad
print '\tAbsoulute Error:', np.abs(modelQuad-analyticalQuad)
print '\tRelative  Error:', (np.abs(analyticalQuad-modelQuad)
                                /analyticalQuad)*100
for i in range(0, len(end)):
    print '\nModel Result After:', end[i], 'Years:', result[i][-1]
    print 'Analytical Result: ', end[i], 'Years:', analytical[i]
    print '\tAbsoulute Error:', np.abs(analytical[i]-result[i][-1])
    print '\tRelative  Error:', (np.abs(analytical[i]-result[i][-1])
                                 /analytical[i])*100

plt.plot(time[-1], result[-1])

for i in range(0, len(end)):
    plt.vlines(end[i],start,result[i][-1])
    plt.hlines(result[i][-1],start,end[i])
    plt.plot(end[i], result[i][-1], 'g.', markersize=10.0)
    plt.text(end[i]-6, result[i][-1], result[i][-1]*1.05)

plt.ylim(starting_cash, (analytical[len(end)-1]*1.1))
plt.xlim(0, end[i]+2)
plt.title('Continous Growth Model')
plt.xlabel('Years')
plt.ylabel('Cash Value')
plt.show()

#plt.savefig('Quayle - Computational Error.png')