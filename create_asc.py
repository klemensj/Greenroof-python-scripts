
# # # # # # # # # # # # # # # # # # #
# The purpose of this code is to create fake AOIs  
## in order to test the behavior and performance of agents 
## in the Greenroofs.nlogo model
#
# To use set 'size', follow on screen instructions 
## Will create a square area of interest (AOI) with side of length 'size'
## populated with circles, squares or scattered green making up a given
## percentage of the total area, and in the case of squares and circles, 
## divided into a given number of shapes
#

import numpy as np
import random as rand
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap 

#some global variables for convenience

size = 2595     # arbitrary for now based on GIS datasets we have had 2595

	
####Function Definitions#######
	
# functions for different dataset generation patterns

#function to draw SCATTER

def Scatter(OutputFile, size, NumberGreen):
	GisData = np.ones( (size,size), dtype='int' )  #create matrix filled with ones


	if PercentGreen==0:                 #if then else for dealing with extremes
		GisData = GisData*5
		print "all black"
	elif PercentGreen==100:
		print "all green"
	else:
		GisData = GisData*5
		counter=0
		while counter<NumberGreen:
			x=rand.randint(0, size-1)
			y=rand.randint(0, size-1)
			if GisData[x,y] == 5:       # if it's a black patch
				GisData[x,y] = 1        # make it green
				counter = counter+1     # only update counter when change made
		print counter	
	WriteAsc(OutputFile, size, GisData)

#function to draw CIRCLE
	
def Circle(OutputFile, size, NumberGreen):
	GisData = np.ones( (size,size), dtype='int' )  #create matrix filled with ones
	GisData = GisData*5							   # make all data points "roofs"
	PatNum = int(raw_input("How many circles?: "))
	Radius = np.sqrt((NumberGreen/(np.pi*PatNum)))
	counter = 0
	Centers = np.zeros(shape=(PatNum,2))			#Create a blank matrix for centers 
	#set random centers that are no closer than Radius to the edge of the area
	while counter < PatNum:
		Centers[counter,0]=rand.randint(np.ceil(Radius), size-np.ceil(Radius))
		Centers[counter,1]=rand.randint(np.ceil(Radius), size-np.ceil(Radius))
	# while loop checks that circles are independent, if not counter
	#fails to update so overwrite existing row of centers next time through
	# this is probably not a very efficient algorithm
		counter2 = 0
		tooclose = 0
		while counter2 < counter:
			s1 = Centers[counter,0]-Centers[counter2,0]
			s2 = Centers[counter,1]-Centers[counter2,1]
			if np.hypot(s1,s2) < 2*Radius:
				tooclose = tooclose + 1    # if any circle too close, this updates
			counter2 = counter2 + 1
			    
		if tooclose == 0:
			counter = counter+1      # no circles too close, update counter
	
	                          # Draw a circle for each location in centers file
	counter = 0 
	print "Radius"             # this is just for development
	print Radius
	while counter < PatNum:
		xpos = int(Centers[counter,0] - Radius)
		ypos = int(Centers[counter,1] - Radius)
		counter2 = 0
		while counter2 <= 2*Radius:
			counter3 = 0
			while counter3<= 2*Radius:
				s1 = xpos-Centers[counter,0]
				s2 = ypos-Centers[counter,1]
				if np.hypot(s1,s2) < Radius:
					GisData[xpos, ypos] =  1    # if in circle, make green
				ypos = ypos + 1
				counter3 = counter3 + 1
			xpos = xpos + 1
			ypos = int(Centers[counter,1] - Radius)	
			counter2 = counter2 + 1
		counter = counter + 1	
		
	WriteAsc(OutputFile, size, GisData)	#call the file writer function
		

#function to draw SQUARE

def Square(OutputFile, size, NumberGreen):
	GisData = np.ones( (size,size), dtype='int' )  #create matrix filled with ones
	GisData = GisData*5
	PatNum = int(raw_input("How many squares?: "))
	Side = int(np.sqrt((NumberGreen/(PatNum))))
	counter = 0
	Corners = np.zeros(shape=(PatNum,2))  # set top left corners
	#set random centers that don't overlap other squares
	while counter < PatNum:
		Corners[counter,0]=rand.randint(0, size-Side)
		Corners[counter,1]=rand.randint(0, size-Side)
	# while loop checks that circles are independent, if not counter
	#fails to update so overwrite existing row of Corners next time through
	# this is probably not a very efficient algorithm
		counter2 = 0
		tooclose = 0
		while counter2 < counter:  # checks if any corner of new square within a previous
			if Corners[counter,0] >= Corners[counter2,0] and Corners[counter,0] <= (Corners[counter2,0]+Side) and Corners[counter,1] >= Corners[counter2,1] and Corners[counter,1] <= (Corners[counter2,1] + Side):
				tooclose = tooclose + 1    # if upper left too close, this updates
				
			if (Corners[counter,0]+Side) >= Corners[counter2,0] and (Corners[counter,0]+Side) <= (Corners[counter2,0]+Side) and Corners[counter,1] >= Corners[counter2,1] and Corners[counter,1] <= (Corners[counter2,1] + Side):
				tooclose = tooclose + 1    # if upper right too close, this updates
				
			if Corners[counter,0] >= Corners[counter2,0] and Corners[counter,0] <= (Corners[counter2,0]+Side) and (Corners[counter,1]+Side) >= Corners[counter2,1] and (Corners[counter,1]+Side) <= (Corners[counter2,1] + Side):
				tooclose = tooclose + 1    # if lower right too close, this updates
				
			if (Corners[counter,0]+Side) >= Corners[counter2,0] and (Corners[counter,0]+Side) <= (Corners[counter2,0]+Side) and (Corners[counter,1]+Side) >= Corners[counter2,1] and (Corners[counter,1]+Side) <= (Corners[counter2,1] + Side):
				tooclose = tooclose + 1    # if lower right too close, this updates
			counter2 = counter2 + 1
			    
		if tooclose == 0:
			counter = counter+1      # no circles too close, update counter
                 
                 ### Draw a square for each corner in matrix 'Corners'
	counter = 0 
	print "Side" 
	print Side
	while counter < PatNum:
		xpos = int(Corners[counter,0])
		ypos = int(Corners[counter,1])
		counter2 = 0
		while counter2 <= Side:
			counter3 = 0
			while counter3<= Side:
				GisData[xpos, ypos] =  1    # if in Square, make green
				ypos = ypos + 1
				counter3 = counter3 + 1
			xpos = xpos + 1
			ypos = int(Corners[counter,1])	
			counter2 = counter2 + 1
		counter = counter + 1	
		
	WriteAsc(OutputFile, size, GisData)	#call the file writer function

# /end functions for different dataset generation patterns




# function to WRITE to .ASC file and create image thumbnail

def WriteAsc(OutputFile, size, GisData):
	header = ('ncols '+ str(size) +'\n')    # make sure to change if AOI not square 
	header +=  ('nrows '+ str(size) + '\n')
	header += ('xllcorner 0000000\n')  	# row of top left corner of AOI
	header += ('yllcorner 0000000\n')  	# column of top left corner of AOI
	header += ('cellsize 0.000093\n')
	header += ('NODATA_value -9999')
	np.savetxt(OutputFile, GisData, header=header, comments = '', fmt='%1.5s')
	
	OutputImage = (OutputFile.rsplit( ".", 1 )[ 0 ] + '.png') 	#name of image thumbnail
	
	GisDataForImage = GisData			#Create a second data array for image thumbnail

	GisDataForImage[0,0]=0				#write values into first line of new array
	GisDataForImage[0,1]=1				## to guarantee data has full range for cmap
	GisDataForImage[0,2]=2
	GisDataForImage[0,3]=3
	GisDataForImage[0,4]=4
	GisDataForImage[0,5]=5
										#create colormap, create plot, write plot 
	cmap = ListedColormap(['brown','green','yellow','gray',  'blue', 'black'], 'indexed')
	plt.imshow(GisDataForImage, cmap=cmap)  
	plt.savefig(OutputImage)
	
	
	
	


# MAIN get INPUT from user and go to appropriate function

OutputFile = raw_input("Enter the name of the output file as filename.asc: ")
PercentGreen = int(raw_input("Enter the percentage green space as an integer 0-100: "))
NumberGreen = (pow(size,2)) * PercentGreen / 100
PatternType = raw_input("Enter the pattern type as (s)catter, (sq)uare, or (c)ircle: ")

if PatternType == 'scatter':   # to distribute to proper function
	Scatter(OutputFile, size, NumberGreen)
elif PatternType == 's':   
	Scatter(OutputFile, size, NumberGreen)
elif PatternType == 'square':
	Square(OutputFile, size, NumberGreen)
elif PatternType == 'sq':
	Square(OutputFile, size, NumberGreen)	
elif PatternType == 'circle':
	Circle(OutputFile, size, NumberGreen)
elif PatternType == 'c':
	Circle(OutputFile, size, NumberGreen)
else: 
	print PatternType, 'is not a recognized pattern'
	exit()






	