################################################################################
#   Name: Tyler Quayle
#   Assignment: Monte Carlo 2, Problem 2
#   Date: April 26, 2016
################################################################################
import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt

def simulate(n_times = 1000, sa = .002):
    """
    Simulate n_times number of days, default is 1,000. SA probability of a 
    casual customer entering the store, defaults to .002
    
    RETURNS: core[], casual[], total[]
    """
    core = np.arange(n_times*20, dtype='float').reshape(n_times,20)
    core[:] = 0
    casual = np.arange(n_times*20, dtype='float').reshape(n_times,20)
    casual[:] = 0
    for i in range(n_times):
        core[i], casual[i] = oneDay(sa)
    total = core+casual
    return core, casual, total
    
def oneDay(sa=.002):
    """
    Simulates 1 day in the 'mall', MU and SIGMA are givin in text, N and P for
    core customers must be calculated. N is given for Casual, P must be
    calculated. P depends on SA and total[previous]
    
    RETURNS: core[], casual[], total[]     
    """
    n_casual = np.array([100.,100.,150.,150.,50.,50.,50.,50.,50.,50.,50.,50.,
    150.,150.,150.,150.,150.,150.,100.,100.])
    p_casual = .002
    mu = n_casual/10.
    
    sigma = np.array(n_casual)
    sigma[sigma==100.] = 2.3
    sigma[sigma==150.] = 2.8
    sigma[sigma==50.] = 1.6
    
    p_core = [1-(sigma[0]**2/mu[0])]
    n_core = [mu[0]/p_core[0]]
    
    core = np.zeros(20)
    core[0] = ra.binomial(n_core[0],p_core[0])
    casual = np.zeros(20)
    casual[0] = .01*n_casual[0]

    for i in np.arange(1, 20):
        p_core.append(1-(sigma[i]**2/mu[i]))
        n_core.append([mu[i]/p_core[i]])
        core[i] = ra.binomial(n_core[i],p_core[i])
        p_casual = sa*((core[i-1] + casual[i-1]))+.01
        casual[i] = (n_casual[i] * p_casual)
    return core, casual
    
def displayMeans(core, casual, total):
    """
    Displays to python output the mean for each 'N_TIMES' day simulation. Broken
    down into the mean for each 1/2 increment over the course of the working day
    11am-9pm. Also loads total into pyplot
    
    RETURNS: n/a
    """
    print '\n\nTime\tMean Core\tMean Casual\tMean Total'
    mean_core = [np.mean(core[:,0])]
    mean_casual= [np.mean(casual[:,0])]
    mean_total= [np.mean(total[:,0])]
    print '1','\t',mean_core[0],'\t\t',mean_casual[0],'\t\t',mean_total[0]
    for i in np.arange(1,20):
        mean_core.append(np.mean(core[:,i]))
        mean_casual.append(np.mean(casual[:,i]))
        mean_total.append(np.mean(total[:,i]))
        
        print i+1,'\t',np.around(mean_core[i],2),'\t\t',\
        np.around(mean_casual[i],2),'\t\t',np.around(mean_total[i],2)
    
    print '-------------------------------------------------------------------'
    print 'Totals','\t',np.around(np.sum(mean_core),2),\
    '\t\t',np.around(np.sum(mean_casual),2),'\t\t',np.around(np.sum(mean_total),2)
    plt.plot(mean_total)

if __name__ == "__main__":   #IF Run from cmd line will execute this
#==============================================================================
# USER ADJUSTABLE    
    N_TIMES= 1000
    P_STEPS = 5
    P_INC = .0002
#==============================================================================  
for i in range(P_STEPS):
    core, casual, total = simulate(N_TIMES,.002+(i*P_INC))
    displayMeans(core,casual,total)


plt.title('Mean Total Customers: P0.002-P'+ str(.002+(P_INC*P_STEPS)) )  
plt.ylabel('Mean Total Customers')
plt.xlabel('Time')
plt.xlim(0,20)
plt.show()