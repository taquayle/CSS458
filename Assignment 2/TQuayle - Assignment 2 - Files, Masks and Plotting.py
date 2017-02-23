################################################################################
# NAME:          Tyler Quayle                                                  #
# ASSIGNMENT:    2                                                             #
# PART:          Files, Masks and plotting                                     #
################################################################################
import os
import numpy as N
import matplotlib.pyplot as plt
#  __location__ code found on stackoverflow.com question post. Link at bottom
# __location__ used to find relative location of script to find file instead of
# writing it to Canopy default address
__location__ = os.path.realpath(os.path.join(os.getcwd(), 
                os.path.dirname(__file__)))
readIn = open(os.path.join(__location__, 'ASFG_Ts.txt'), 'r')
errorFile = open(os.path.join(__location__, 'Bad_Data.txt'), 'w')
successFile = open(os.path.join(__location__, 'Successful_Data.txt'), 'w')

data = readIn.readlines() # Get every line from ASFG_Ts.txt and put into a list

julDate = [] # Julian Date List
lat = [] # Latitude List
lon = [] # Longitude List
tem = [] # Temperature List

# Go thru data list, find any bad data and append to Bad_Data.txt. any 'good' 
# data, append to Successful_Data.txt.
for j in data: 
    try:
        err_check = j.split("\t")
        #Check to see if any of the split items contain nothing in the case that
        # there are the correct amount of \t's but nothing inbetween
        if(float(err_check[1]) != None and      
            float(err_check[2]) != None and 
            float(err_check[3]) != None):
            # Append the 'good' data to the correct lists
            julDate.append(float(err_check[0]))
            lat.append(float(err_check[1]))
            lon.append(float(err_check[2]))
            tem.append(float(err_check[3]))
            successFile.write(j)
    except ValueError: # The split function found words, not numbers
        errorFile.write(j)
    except IndexError: # The split function did not find 4 pieces of dats
        errorFile.write(j)

mean = sum(tem)/len(tem) # find Mean of Temp list.
median = N.median(tem) # Find median of Temp list, didn't know
deviation = (sum([(i-mean)**2 for i in tem])/(len(tem)))**.5

print("Records read in: ", len(data))
print("Number of good Records: ", len(tem))
print("Temp Mean: ", mean)
print("Temp Median: ", median)
print("Standard Deviation: ", deviation)

# Creat plot with date being X-Axis and Y-Axis being recorded temp for that date
plt.plot(julDate, tem) 
plt.xlabel("Julian Date")
plt.ylabel("Temp")
plt.title("Surface Heat Budget of the Arctic")
plt.show()

# CLOSE ALL FILES
readIn.close()
errorFile.close()
successFile.close()
# http://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script