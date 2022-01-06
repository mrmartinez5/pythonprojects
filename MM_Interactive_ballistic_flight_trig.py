# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 18:47:55 2021

@author: michaelmartinez
"""
#########################################################################################################################################
#This program asks the user for the initial velocity and angle of a ball shot and uses trig functions to computes the maximum vertical height 
#and horizontal distance that a ballistic missile travels in ideal conditions. #
#########################################################################################################################################

import math #calls math libraries
g = 9.8 #gravitational acceleration m/s 
pi = float(22/7)

def Repeat(): #this function repeats the calculator or terminates the program depending on the user input
    decision=input("Do you want to calculate again? Y/N \n") #the user inputs a choice, hopefully Y or N
    if decision == "": #checks if the user entered nothing
        print("Sorry, not a valid entry. Enter Y/N \n")
        Repeat() #repeats the Y/N process
    if decision.isdigit(): #checks if the user entered a number
        print("Sorry, not a valid entry. Enter Y/N \n")
        Repeat() #repeats the Y/N process
    if decision == "y": #checks for little y as a yes
        inputVelocity() #loops back to the beginning of the calculator
    if decision == "Y": #checks for big Y as a yes
        inputVelocity() #loops back to the beginning of the calculator
    if decision == "n": #checks for little n as a no
        print("Thank you for using my program! \n")
    if decision == "N": #checks for big N as a no
        print("Thank you for using my program! \n")
        
def missilePathTrig(v0, alpha): #this function calculates the ballistic flight of the shot using user-specified v0 and alpha values
    alphaRadians = float(alpha * (pi/180)) #here we convert to radians from degrees behind the scenes
    xm = float(2*v0*math.cos(alphaRadians)*((v0*math.sin(alphaRadians))/g)) # the horizontal distance the ball travels - we want to know this as a fx of any given v0,alpha
    roundXm = round(xm, 3) # I learned to round from: https://www.youtube.com/watch?v=uYSvspYbwxc
    ym = float((1/2)*(((v0*math.sin(alphaRadians))**2)/g)) # the maximum height the ball travels - we want to know this as a fx of any given v0,alpha
    roundYm = round(ym, 3) # I learned to round from: https://www.youtube.com/watch?v=uYSvspYbwxc
    print("The max. horizontal distance (xm) is", roundXm, "meters, and the max. vertical height (ym) is", roundYm,"meters.") #outputs the calculated xm and ym values
    Repeat() #determines if the user wants to repeat or terminate

def angleAlpha(v0,alpha): #function to verify the user inputs for angle alpha     
    alpha = input("Input the initial angle from the horizontal, a (alpha), from 0-90° in decimal degrees. Example: 41.235° \n") #asks the user to input the initial angle from the horizon in decimal degrees.
    if alpha.isalpha(): #rejects inputs that are not at least a number #looked up some help from https://stackoverflow.com/questions/40097590/detect-whether-a-python-string-is-a-number-or-a-letter
        print("Sorry, not a valid entry. Try again.")
        angleAlpha(v0,alpha) #returns v0,alpha to the function and loops over again
    if float(alpha) > 90: #checks if the angle is greater than 90 and asks the user to try again if so
        print("We need a trajectory that shoots forwards!")
        angleAlpha(v0,alpha) #returns v0,alpha to the function and loops over again
    if float(alpha) < 0: #checks if the angle is less than 0 and asks the user to try again if so
        print("We need a trajectory that shoots into the sky!")
        angleAlpha(v0,alpha) #returns v0,alpha to the function and loops over again
    else: #all other cases should be OK to move forward with calculations
        print("\n This input is acceptable. You entered:", alpha, "for your alpha angle. \n")
        a = float(alpha) #converts user alpha to type(float) after logic checks are done
        missilePathTrig(v0, a) #sends v0,alpha to calculate ballistic flight
        
def inputVelocity(): #function to verify the user inputs for the initial velocity. 
    alpha = 0 #gave alpha a beginning value of 0 - will be overwritten by user
    v0 = input("Input the initial velocity, (v0), in decimal format. Example: 10.567 \n") #asks the user to input the initial velocity and expects a decimal number.    
    if v0 == "": #Special case when the user just hits enter. Help from: https://stackoverflow.com/questions/23979184/how-to-know-if-a-user-has-pressed-the-enter-key-using-python
        print("Sorry, not a valid entry. Try again.")
        inputVelocity() #reloops this function for a failed attempt
    if v0.isalpha(): #Rejects inputs that are not at least a number #looked up some help from https://stackoverflow.com/questions/40097590/detect-whether-a-python-string-is-a-number-or-a-letter
        print("Sorry, not a valid entry. Try again.")
        inputVelocity() #reloops this function for a failed attempt
    if float(v0) <= 0: #Rejects inputs that are not positive velocities
        print("We need a positive initial velocity to fly!")
        inputVelocity() #reloops this function for a failed attempt
    else: #else, everything is fine and move forward
        print("\n This input is acceptable. You entered:", v0, "for your initial velocity.")
        vi=float(v0) #converts user v0 to type(float) after logic checks are done.
        angleAlpha(vi,alpha) #sends v0,alpha to angleAlpha function.
        

inputVelocity()

