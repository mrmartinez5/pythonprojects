The script takes in user inputs for the number of subsurface layers, their thicknesses and seismic velocities, checks that they're valid inputs, 
and then returns an offset vs traveltime pyplot. The script also outputs the offsets and traveltimes to .csv format in the project folder.

The script takes advantage of arrays and broadcasting to handle an "infinite" amount of cases specified by the user.
