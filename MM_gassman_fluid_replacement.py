# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 21:37:16 2021

@author: metam
"""
# This script reads in values from a .csv and uses Gassmann's equation to compute the dry frame bulk modulus and the oil-saturated P-wave velocity
# and finally saves the sample number and predicted velocity in a two-column csv.
# This script uses numpy ndarrays as the main data format

import numpy as np

data = np.loadtxt('Z:/OneDrive/University/UH Geology/Graduate/Coursework/2021 FALL/GEOL6322/Week 5/17_dry_samples.csv', delimiter = ",") #imports the raw data from the .csv
sampleNo = data[:,0]            #stores the first column as an ndarray
H2OsampleDensity = data[:,1]    #stores the next column as an ndarray...
H2OsampleVp = data[:,2]         #...
H2OsampleVs = data[:,3]         #...
samplePorosity = data[:,4]      #...
matrixDensity = data[:,5]       #...
Kmatrix = data[:,6]             #stores the final column as an ndarray, also known as Ko

#given bulk modulus and density for water(H2O) and oil, where K is bulk modulus
H2OKfluid = 1.96e9 #bulk modulus of water, [GPa]
oilKfluid = 1.26e9 #bulk modulus of oil, [GPa]
H2Odensity = 1000  #kg/m^3
oildensity = 830   #kg/m^3

predictedVps = np.ones(17) #initialize a ones array for my predicted oil-saturated Vp values

#loops 17 times to populate new array predictedVps for oilsampleVp
for i in range(17): 
    Mu = (H2OsampleVs[i]**2) * H2OsampleDensity[i] #1 Solve for Mu (Shear Modulus) using H2OsampleVs and H2OsampleDensity
    H2OKsat = (H2OsampleVp[i]**2) * H2OsampleDensity[i] - ((4/3) * Mu) #2 Solve for water-saturated bulk modulus (H2OKsat) using H2OsampleDensity, Mu, H2OsampleVp
    Kframe = ((H2OKsat * ((samplePorosity[i] * Kmatrix[i])/H2OKfluid) + 1 - samplePorosity[i]) - Kmatrix[i]) / (((samplePorosity[i] * Kmatrix[i]) / H2OKfluid) + (H2OKsat/Kmatrix[i]) - 1 - samplePorosity[i]) #3 Solve for empty frame bulk mod (Kframe or K*) using H2OKsat, Kmatrix (also Ko), H2OKfluid (provided in prompt), samplePorosity
    oilKsat =  Kframe + (((1 - (Kframe/Kmatrix[i]))**2) / ((samplePorosity[i]/oilKfluid) + ((1-samplePorosity[i])/Kmatrix[i]) - (Kframe / Kmatrix[i]**2))) #4 Solve for oilKsat (oil saturated bulk mod) using Kframe, matrixBulkmod, Koil (prompt), samplePorosity     
    oilsampleDensity = (matrixDensity[i] * (1 - samplePorosity[i])) + (oildensity * samplePorosity[i]) #5 Solve for oilsampleDensity using samplePorosity, oildensity, matrixDensity 
    oilsampleVp = np.sqrt((oilKsat + (4/3)*Mu)/oilsampleDensity) #6 Solve for predictedVp using oilKsat, Mu, oilsampleDensity
    predictedVps[i] = oilsampleVp
       
#Finally, write out into 2 columns of a csv file - 1) sampleNo array 2) predictedVps array
calculations = np.column_stack([sampleNo,predictedVps]) #prepares my two arrays as columns
labels = ['sample number', 'predicted oil-saturated Vp'] #prepares simple labels for my columns
labelrow = ','.join(labels) #formats the display for my header labels
np.savetxt('Z:/OneDrive/University/UH Geology/Graduate/Coursework/2021 FALL/GEOL6322/Week 5/output results.csv', calculations, fmt = '%0.04f', delimiter = ",", header = labelrow) #outputs the data to .csv




