
# # # # # # # # # # # # # # # # # # #
# The purpose of this code is to extract multiple areas of interest 
## from the greenroofascii.txt file, which is a raster land use map
## at 1 foot resolution of the city of Philadelphia,
## and also to generate a thumbnail image of the AOI
#
# To use set 'clipsize'.  Will create a square area of interest (AOI) 
## with side of length 'clipsize'. 
#
# Also set range of files to be generated with the range of the enclosing for loop
## File names will be AOI_rand_i.asc where i is set by the for loop


import numpy as np
import random as rand
import matplotlib.pyplot as plt
#import matplotlib as mpl
from matplotlib.colors import ListedColormap 


AOIStart = int(raw_input("Enter a number for the first AOI: "))
AOINumber = int(raw_input("Enter the number of AOIs to generate: "))

							# comment out line below to automate
							# or make regularly spaced AOIs


clipsize=2595                 # 2595 is value of original AOI file, somewhat arbitrary
							  # single value b/c square matrices, update if needed

xsize = 97744                 #these values specific to greenroofascii.txt
ysize = 89539 

for i in range(AOIStart,AOIStart+AOINumber):
	
	OutputFile = ('AOI_rand_'+ str(i) +'.asc')
	OutputImage = ('AOI_rand_'+ str(i) +'.png') 	#name of image thumbnail

	# rowx and coly are the row and column of the upper left corner of the 
	## area of interest. Base version sets a random AOI, 
	## to create regularly spaced AOIs replace the two lines below with a loop 

	rowx=  rand.randint(6, xsize-clipsize+6) # +6  accounts for six line header and
	coly=  rand.randint(0, ysize-clipsize)    ## -clipsize keeps AOI within file



	counter = 0 							  # this while loop walks down to a random line
	f = open('greenroofascii.txt', 'r')
	while counter < rowx :                  
		f.readline()                           #f.readline() reads and goes to next row
		counter = counter+1

	data=[]
	counter = 0	
	while counter < clipsize :                 # this while loop pulls in individual
		data.append(f.readline())			   ## lines from the datasets based on 'rowx'
		counter = counter+1
												# the next line converts the data to an array
												## the usecols function selects 
												## columns based on 'coly' value
											
	GisData = np.genfromtxt(data, dtype='int', usecols=range(coly, coly+clipsize))

	# Reporter functions to check that everything ran, can probably be done away with 

	print '\n' 'datamatrix size: ', GisData.shape
	print 'rowx : ', rowx, 'coly : ', coly, '\n'
	f.close()

	#clippedfile = open(OutputFile, 'w')
	header = ('ncols '+ str(clipsize) +'\n')    # make sure to change if AOI not square 
	header +=  ('nrows '+ str(clipsize) + '\n')
	header += ('xllcorner ' + str(rowx) + '\n')  	# row of top left corner of AOI
	header += ('yllcorner ' + str(coly) + '\n')  	# column of top left corner of AOI
	header += ('cellsize 0.000093\n')
	header += ('NODATA_value -9999')
	np.savetxt(OutputFile, GisData, header=header, comments = '', fmt='%1.5s')
	
	GisDataForImage = GisData			#Create a second data array for image thumbnail
	
	GisDataForImage[0,0]=-1
	GisDataForImage[0,1]=0				#write values into first line of new array
	GisDataForImage[0,2]=1				## to guarantee data has full range for cmap
	GisDataForImage[0,3]=2
	GisDataForImage[0,4]=3
	GisDataForImage[0,5]=4
	GisDataForImage[0,6]=5
										#create colormap, create plot, write plot 
	cmap = ListedColormap(['brown','cyan','green','yellow','gray',  'blue', 'black'], 'indexed')
	plt.imshow(GisDataForImage, cmap=cmap)  
	plt.savefig(OutputImage)
	
	print "Done"