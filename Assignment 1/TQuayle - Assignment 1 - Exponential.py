################################################################################
# NAME:          Tyler Quayle                                                  #
# ASSIGNMENT:    1                                                             #
# PART:          Distance                                                      #
################################################################################
import math as M
# exponential(num, tol)
# Take in num, using a loop to calculate the series (num^n)/n!. Within a
# tolerance of tol, since you cannot calculate an infinite series 
def exponential(num, tol):    
    result = 0.0 # Final result
    temp_result = 0.0 # used to find tol_check, previous loops result
    tol_check = num # used to find number within tolerance range
    n = 0 # used to track step in series.   
    
    # Loop until check is less than tolerance, indicating tolerance met
    while tol_check > tol:
        result += float(M.pow(num, n)/M.factorial(n))
        tol_check = (result-temp_result)
        temp_result = result
        n += 1
    return result

################################################################################
# Execute
if __name__ == "__main__":   
    print(exponential(3.4, tol=1e-12))
    