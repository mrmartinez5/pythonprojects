# -*- coding: utf-8 -*-
"""
Created on Tue Jan 04 00:10:00 2022
@author: metam

*This script calculates the travel times and offsets associated with 
seismic wave reflections within a user-specified number of layers 
following this ideal method:
    
*Note: Script assumes take-off angles (alpha_angle) 
from 0-90 degrees in 1 degree intervals. 

Recall that take-off angle = incidence angle = reflected angle.

1 - The script asks the user to input the desired amount of layers 
and associated thicknesses and velocities
and tries to check those inputs to make sure they're valid. 

2 - Uses Snell's law (sin i / v1) = (sin r / v2) 
to calculate the critical angle(crit_angle), 
where crit_angle = arcsin(v1/v2) and refraction angle of the layer below.

**3 - Calculates offset and travel time for the all primary reflections.

4 - The results are saved and output in a CSV file 
called "MultiLayerResults.csv" located in the same directory as the script.

5 - The results are plotted in a line graph of offset vs tvt, 
with offset = total thickness of layer system

Special notes:
       
**The script will output a special exception case for angles 
that produce a total reflection between the two layers.

This script uses numpy arrays and broadcasting 
and tries to avoid for loops per the instructions.

@author: Michael R. Martinez
"""

############################### IMPORTS ######################################

import numpy as np
import matplotlib.pyplot as plt
import csv

########################### GLOBAL VARIABLES #################################

# Populate array with the take-off angles from 0-90 degrees 
# by 1 degree increments - includes 90°
takeoff_angles = np.arange(0, 91, 1) 
n_takeoff_angles = len(takeoff_angles)

#Use deg2rad to convert decimal degrees into radians
alpha_angles = np.deg2rad(takeoff_angles)

############################## FUNCTIONS #####################################

#data ingestion functions#
def positive_integer(userinput):
    '''Asks for a keyboard input until a non-negative integer is given.'''
    value = None #initialize value as None
    while not value: #while not "none"
        try: #requests positive integer
            value = int(input('Please enter a positive integer number: ')) 
        except ValueError: #catches non-integer inputs
            print('Please enter an integer number: ')
        else:
            if (value <= 0): #catches negative integers
                print('Please enter a positive integer number: ')
                value = None #resets value to none to rerun the loop
            else:
                print('You entered', value, '.') #confirms valid user input
    return(value) 

def positive_float(userinput): #reused the function above but edited for float
    '''Asks for a keyboard input until a non-negative float is given.'''
    value = None #initialize value as None
    while not value: #while not "none"
        try: #requests positive integer
            value = float(input('Please enter a positive float number: ')) 
        except ValueError: #catches non-integer inputs
            print('Please enter a positive float number: ')
        else:
            if (value <= 0): #catches negative integers
                print('Please enter a positive float number: ')
                value = None #resets value to none to rerun the loop
            else:
                print('You entered', value, '.') #confirms valid user input
                print('\n')
    return(value) 

# data processing functions#
def compute_offset(thickness, angle):
    '''Returns total offset traveled in this layer.'''
    return(2 * thickness * np.tan(angle))

def compute_tvt(thickness, angle, speed):
    '''Returns total traveltime spent in this layer.'''
    ray_distance = 2 * (thickness / np.cos(angle))
    layer_travel_time = ray_distance / speed
    return(layer_travel_time)

def snells(incident_angle, incident_speed, refracted_speed):
    '''Return angle of refraction if subcritical, NaN if supercritical.'''
    return(np.arcsin(refracted_speed / 
                     incident_speed * np.sin(incident_angle)))

def compute_angle_of_propagation(alpha_angles, speeds, n_layers):
    '''Return takeoff angles for all layers as an array of radian angles'''
    #creates an empty array to be filled with angles of propagation
    rad_angles = np.empty((n_layers, len(takeoff_angles)))
    #convert takeoff angles into radians
    #angle of propagation in the 1st layer "rad_angles[0]" 
    #is the same as the takeoff angle
    rad_angles[0] = alpha_angles
    #calculate angle of propagation in subsequent layers 
    #using snell's law function above
    for i in range(1, n_layers):
        rad_angles[i] = snells(rad_angles[i-1], speeds[i-1], speeds[i])
    return rad_angles #returns the complete set of angles of propagation


################################ MAIN ########################################      
'''Main portion captures number of layers, thicknesses, velocities, 
and outputs results in csv and plot form'''

# capture number of layers from the user
print('Please input your desired number of subsurface layers below.')
userinput = None
n_layers = positive_integer(userinput)
print('You specified', n_layers, 'number of subsurface layers.')
print('\n')
# at this point, we have total # of layers (n_layers) and takeoff_angles

# initialize velocity and thickness arrays as empty arrays
speeds = np.empty(n_layers)
thicknesses = np.empty(n_layers)

# capture layer velocities and thicknesses and fill respective arrays
for i in range(n_layers):
    userinput = None
    print('Please enter velocity [m/s] as a positive float for layer %d' % (i+1), 'below.')
    speeds[i] = positive_float(userinput)

    userinput = None
    print('Please enter thickness [meters] as a positive float for layer %d' % (i+1), 'below.')
    thicknesses[i] = positive_float(userinput)
    
# compute total thickness
total_thickness = np.sum(thicknesses, axis=None)
# check for sum
print('The total thickness of the system is:', total_thickness) 
print('\n')

# initialize offsets and tvt arrays
offsets = np.empty((n_layers, n_takeoff_angles))
traveltimes = np.empty((n_layers, n_takeoff_angles))

# calculate angles of propagation and fill array
angles_of_propagation = compute_angle_of_propagation(alpha_angles, 
                                                     speeds, 
                                                     n_layers)

# "reshape" with a dummy axis thicknesses array for broadcasting  
  
offsets = compute_offset(thicknesses[:, np.newaxis], angles_of_propagation)
total_offsets = np.sum(offsets, axis=1)

traveltimes = compute_tvt(thicknesses[:, np.newaxis], angles_of_propagation, 
                          speeds[:, np.newaxis])

total_traveltimes = np.sum(traveltimes, axis=1)

############################### PLOTS ########################################
# unpack tuple into variables fig and ax
fig, ax = plt.subplots()

# plot offsets vs traveltimes, but transpose the arrays
ax.plot(offsets.T, traveltimes.T)

# set x-axis limits
ax.set_xlim(0, total_thickness)
# label x-axis
ax.set_xlabel('Offset')

# set y-axis limits
ax.set_ylim(0,3.5)
# label y-axis
ax.set_ylabel('Travel time')

#I tried to troubleshoot the odd case where the 2nd reflection arrives sooner
#than the 1st reflection. I am not sure why it's solving that way -_-

################################ CSV #########################################
# shaping an array for output to csv
# rows = # of take-off angles
# columns = 1 for take-off angles + # of offsets + # of traveltimes
columns = 2 * len(offsets) + 1
results_size = (len(takeoff_angles), columns)

# initial results array, filled with ones
results = np.ones(results_size)

# initialize column headers, start with take-off angles
columnHeaders = ['take-off angle'] 

# fills first column with take-off angles
results[:,0] = takeoff_angles

# fills columns with offsets
for i in range(len(offsets)):
    results[:, i+1] = offsets[i] #shift 1 column for take-off angles
    # write custom headers for offsets
    columnHeaders.append('offset %d' % (i+1))

# column shift equal to # of columns for offsets + take-off angles
BeginTVTheader = len(offsets) + 1
# fills shifted columns with traveltimes
for i in range(BeginTVTheader, columns):
    results[:, i] = traveltimes[i-BeginTVTheader]
    # write custom headers for traveltimes
    columnHeaders.append('traveltime %d' % (i+1-BeginTVTheader))

# gives more details about NaN supercritical values (alpha_angle > crit_angle)
results = np.where(np.isnan(results), 
                   ["Total reflection case"], results)    

# define the output csv filename
filename = "MultiLayerResults.csv" 
        
# writing to the CSV file
with open(filename, 'w', newline = '') as csvfile:             
    #creating a csv writer object
    csvwriter = csv.writer(csvfile)
    #writing the header
    csvwriter.writerow(columnHeaders)
    #writing the data rows
    csvwriter.writerows(results)      

