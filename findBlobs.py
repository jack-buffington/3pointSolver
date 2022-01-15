import cv2 as cv
#import apriltag
import numpy as np
import sys







class lineMatch:
	xMin: int = 0
	xMax: int = 0 
	xWeight: int = 0
	isActive: bool = False
	whichBlob: int = -1		# Used when adding lineMatches to blobs if they overlap with a previous line
	def __init__(self, xMin = 0, xMax = 0, xWeight = 0, isActive = False, whichBlob = -1):  
		self.xMin = xMin
		self.xMax = xMax
		self.xWeight = xWeight
		self.isActive = isActive
		self.whichBlob = whichBlob 


class blob:
	xMin: int = 0
	xMax: int = 0
	yMin: int = 0
	yMax: int = 0
	xWeight: int = 0
	yWeight: int = 0 
	centroidX: float = 0.0
	centroidY: float = 0.0
	pixelCount: int = 0
	blobID: int = 0 




def findBlobs(theImage):
	# Returns a list of the blobs that were found in the image
	# theImage is a pre-processed image that is just black or white where white represents a 
	# region that I am interested in.

	blobIndex = 0
	blobLocator = {} # this is a dictionary of blobIDs associated with their index.

	#print(f"Width: {theImage.shape[1]}  Height: {theImage.shape[0]}" )
	rows = theImage.shape[0]
	cols = theImage.shape[1]

	lastRow = []

	lm = lineMatch()
	activeBlobs = []
	completedBlobs = []

	for y in range(rows):
		thisRow = []
		#print(" ")
		#print(f"Working on row {y}")
		for x in range(cols):
			##############################################################################################
			# for each scanline, look for ranges of pixels that are white and create lineMatches from them
			##############################################################################################
			if theImage[y,x] == 255:
				if lm.isActive == False:
					lm.isActive = True 
					lm.xMin = x 
					lm.xMax = x
					lm.xWeight = x
				else:
					lm.xMax = x
					lm.xWeight += x
			else: # this is a black pixel
				if lm.isActive == True:
					# copy the lineMatch into thisRow and set it to inactive
					thisRow.append(lineMatch(lm.xMin, lm.xMax, lm.xWeight, False, -1))	
					lm.isActive = False
		# Check to see if it was currently doing a line match when it finished the row.  If so then complete the lineMatch
		if lm.isActive == True:
			lm.isActive = False
			thisRow.append(lineMatch(lm.xMin, lm.xMax, lm.xWeight, False, -1))	
		


		################################################################################################### 
		# It is done going through a row and creating line matches.  Now compare each match to the previous
		# Row's line matches and determine if there are any overlaps.  If there are, add these matches into 
		# the same blobs.  If there aren't any overlaps then create a new blob that contains the match
		###################################################################################################

		for thisLineMatchNumber in range(len(thisRow)):
			# There is an overlap if the start of the last line match <= the end of this line's match 
			#	and the start of this line's match is <= the end of the last line's match
			thisMatch = thisRow[thisLineMatchNumber]
			for lastLineMatchNumber in range(len(lastRow)):
				lastMatch = lastRow[lastLineMatchNumber]
				# compare the two to see if there is overlap
				if (lastMatch.xMin <= thisMatch.xMax) and (thisMatch.xMin <= lastMatch.xMax):
					# then there is an overlap.

					thisBlobID = thisMatch.whichBlob 
					if thisBlobID == -1:
						thisBlobIndex = -1 # this line probably not needed.   Leaving it here for clarity.
					else:
						thisBlobIndex = blobLocator[thisBlobID] 
					oldBlobID = lastMatch.whichBlob
					oldBlobIndex = blobLocator[oldBlobID]

					

					if thisBlobID == -1:	# It overlapped but hasn't been added to a blob yet
						thisRow[thisLineMatchNumber].whichBlob = oldBlobID
						if activeBlobs[oldBlobIndex].xMin > thisMatch.xMin:
							activeBlobs[oldBlobIndex].xMin = thisMatch.xMin
						if activeBlobs[oldBlobIndex].xMax < thisMatch.xMax:
							activeBlobs[oldBlobIndex].xMax = thisMatch.xMax
						activeBlobs[oldBlobIndex].yMax = y 
						activeBlobs[oldBlobIndex].xWeight += thisMatch.xWeight
						matchPixelCount = thisMatch.xMax - thisMatch.xMin + 1
						activeBlobs[oldBlobIndex].yWeight += matchPixelCount * y
						activeBlobs[oldBlobIndex].pixelCount += matchPixelCount

					else: # It overlapped but was already added to another blob.   Check to see if the overlap is with a different blob.  
						if thisBlobID != lastMatch.whichBlob:
							# It is a different blob so add the other blob to this blob, change the previous line's linematch 
							# to be the new blob, and get rid of the old blob. 
							lastRow[lastLineMatchNumber].whichBlob = thisBlobID # change the previous lineMatch's blob
							# merge the two blobs
							if activeBlobs[thisBlobIndex].xMin > activeBlobs[oldBlobIndex].xMin:
								activeBlobs[thisBlobIndex].xMin = activeBlobs[oldBlobIndex].xMin
							if activeBlobs[thisBlobIndex].xMax < activeBlobs[oldBlobIndex].xMax:
								activeBlobs[thisBlobIndex].xMax = activeBlobs[oldBlobIndex].xMax
							activeBlobs[thisBlobIndex].xWeight += activeBlobs[oldBlobIndex].xWeight
							activeBlobs[thisBlobIndex].yWeight += activeBlobs[oldBlobIndex].yWeight
							activeBlobs[thisBlobIndex].pixelCount += activeBlobs[oldBlobIndex].pixelCount
					
			# Check to see if it was added to a blob in the previous steps.  If it wasn't then create a new blob and add it to that.			
			if thisRow[thisLineMatchNumber].whichBlob == -1:
				pixelCount = thisMatch.xMax - thisMatch.xMin + 1
				
				tempBlob = blob()
				tempBlob.xMin = thisMatch.xMin
				tempBlob.xMax = thisMatch.xMax
				tempBlob.yMin	= y
				tempBlob.yMax = y
				tempBlob.xWeight = thisMatch.xWeight
				tempBlob.yWeight = pixelCount * y
				tempBlob.pixelCount = pixelCount
				tempBlob.blobID = blobIndex
				
				thisMatch.whichBlob = blobIndex
				blobIndex += 1
				activeBlobs.append(tempBlob)



		lastRow = thisRow

		# get ready for the next row
		# Go through all of the active blobs.  If their maxY is less than y then copy those 
		# blobs to completed blobs and then delete them from the activeBlob list.
		for I in reversed(range(len(activeBlobs))): # go through them backwards so deleting won't cause me to miss one.
			if(activeBlobs[I].yMax != y):
				completedBlobs.append(activeBlobs[I])
				del activeBlobs[I]

		# Rebuild the blobLocator dictionary for the next loop
		# The blobLocator dictionary is blobLocator[<blobID>] = <index of that blob in activeBlobs>
		blobLocator.clear()
		for I in range(len(activeBlobs)):
			blobLocator[activeBlobs[I].blobID] = I

		
	# At this point it is done scanning through the image.  Move any remaining active blobs into the completedBlobs
	for I in range(len(activeBlobs)):
		completedBlobs.append(activeBlobs[I])
	
	# compute the blob centroids
	for I in range(len(completedBlobs)):
		# TODO:  Verify that the centroids are floats
		completedBlobs[I].centroidX = completedBlobs[I].xWeight / completedBlobs[I].pixelCount
		completedBlobs[I].centroidY = completedBlobs[I].yWeight / completedBlobs[I].pixelCount

	# Print out some info about the blobs

	# print("\n\ncompleted finding the blobs.  Here is what was found:")
	# for I in range(len(completedBlobs)):
	# 	print(f"Blob #{I}:")
	# 	print(f"   xMin: {completedBlobs[I].xMin}   xMax: {completedBlobs[I].xMax}")
	# 	print(f"   yMin: {completedBlobs[I].yMin}   yMax: {completedBlobs[I].yMax}")
	# 	print(f"   centroidX: {completedBlobs[I].centroidX}   centroidY: {completedBlobs[I].centroidY}")
	# 	print(f"   xWeight: {completedBlobs[I].xWeight}   yWeight: {completedBlobs[I].yWeight}")
	# 	print(f"   pixelCount: {completedBlobs[I].pixelCount}")


	return completedBlobs





















minHue = 0
maxHue = 30

# print(f"Arguments count: {len(sys.argv)}")
# for i, arg in enumerate(sys.argv):
# 	print(f"Argument {i:>6}: {arg}")
# 	if i == 1:
# 		minHue = int(arg)
# 	if i == 2:
# 		maxHue = int(arg)


print("Run with:\npython3 findBlobs.py <video file's base name>")
fileBase = sys.argv[1]
#fileBase = input("What is the video file's base name?  (without .mp4) ")

#fileBase = "straightLineWhileChangingDirections670x690"
inFileName = fileBase + ".mp4"
outFileName = fileBase + ".txt"

print(f"In: {inFileName}\n")
print(f"Out: {outFileName}\n")



print("Starting up...")
#vid = cv.VideoCapture("s9video.mp4")
#vid = cv.VideoCapture("apriltags01.mp4")
#vid = cv.VideoCapture("apriltags02.mp4")
#vid = cv.VideoCapture("circleTriangleSquare600_760.mp4")
vid = cv.VideoCapture(inFileName)

file1 = open(outFileName,"w")
file1.write("blueX, blueY, orangeX, orangeY, greenX, greenY, redX, redY, robotX, robotY, robotAngle\n")

# Check if camera opened successfully
if (vid.isOpened()== False):
	print("Error opening video stream or file")

frameCount = 0

while(vid.isOpened()):
	# # Skip over a bunch of frames each time.
	# for I in range(15):
	# 	ret, frame = vid.read()

	try:
		ret, frame = vid.read()


		if ret == True:
			print(f"Processing frame {frameCount}")
			frameCount += 1
			hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)	#hsv is a numpy.ndarray

			# do some thresholding using numpy.

			#(r, g, b) = cv.split(frame)

			(h, s, v) = cv.split(hsv)  #Split into individual channels
			out2 = np.ones(np.shape(h)) * 255

			

			# Create some images that are black or white indicating where the colors that I am interested in are located:
			red = (( ((h > 110) + (h < 5)) * (s > 190) * (v > 140) * (v < 170)) * out2).astype(np.uint8)   
			neonBlue = ((h > 95) * (h < 118) * (s > 110) * (s < 140) * (v > 105) * (v < 165) * out2).astype(np.uint8)    
			orange = ((h > 3) * (h < 20) * (s > 145) * (v > 160) * (v < 215)  * out2).astype(np.uint8)   
			holidayGreen = ((h > 35) * (h < 85) * (v > 35) * (v < 70) * (s > 125) * (s < 210) *out2).astype(np.uint8)   
			



			# # search for blobs


			# redBlobs = findBlobs(red)
			# print("Done with red")


			neonBlueBlobs = findBlobs(neonBlue)
			print("Done with blue")
			orangeBlobs = findBlobs(orange)
			print("Done with orange")
			holidayGreenBlobs = findBlobs(holidayGreen)
			print("Done with green")


			maxPixelCount = 0
			biggestRedBlob = -1



			maxPixelCount = 0
			biggestBlueBlob = -1
			for I in range(len(neonBlueBlobs)):
				if neonBlueBlobs[I].pixelCount > maxPixelCount:
					maxPixelCount = neonBlueBlobs[I].pixelCount
					biggestBlueBlob = I

			maxPixelCount = 0
			biggestOrangeBlob = -1
			for I in range(len(orangeBlobs)):
				if orangeBlobs[I].pixelCount > maxPixelCount:
					maxPixelCount = orangeBlobs[I].pixelCount
					biggestOrangeBlob = I

			maxPixelCount = 0
			biggestGreenBlob = -1
			for I in range(len(holidayGreenBlobs)):
				if holidayGreenBlobs[I].pixelCount > maxPixelCount:
					maxPixelCount = holidayGreenBlobs[I].pixelCount
					biggestGreenBlob = I

			# # Draw a rectange around each max
			# cv.rectangle(frame,(redBlobs[biggestRedBlob].xMin, redBlobs[biggestRedBlob].yMin),(redBlobs[biggestRedBlob].xMax, redBlobs[biggestRedBlob].yMax),(0,0,255),3)
			cv.rectangle(frame,(neonBlueBlobs[biggestBlueBlob].xMin, neonBlueBlobs[biggestBlueBlob].yMin),(neonBlueBlobs[biggestBlueBlob].xMax, neonBlueBlobs[biggestBlueBlob].yMax),(255,0,0),3)
			cv.rectangle(frame,(orangeBlobs[biggestOrangeBlob].xMin, orangeBlobs[biggestOrangeBlob].yMin),(orangeBlobs[biggestOrangeBlob].xMax, orangeBlobs[biggestOrangeBlob].yMax),(0,128,255),3)
			cv.rectangle(frame,(holidayGreenBlobs[biggestGreenBlob].xMin, holidayGreenBlobs[biggestGreenBlob].yMin),(holidayGreenBlobs[biggestGreenBlob].xMax, holidayGreenBlobs[biggestGreenBlob].yMax),(0,255,0),3)



			file1.write(f"{neonBlueBlobs[biggestBlueBlob].centroidX}, {neonBlueBlobs[biggestBlueBlob].centroidY}, {orangeBlobs[biggestOrangeBlob].centroidX}, {orangeBlobs[biggestOrangeBlob].centroidY}, {holidayGreenBlobs[biggestGreenBlob].centroidX}, {holidayGreenBlobs[biggestGreenBlob].centroidY}, 0, 0, 0, 0, 0\n")



			#cv.imshow('red', red)
			#cv.imshow('blue', neonBlue)
			#cv.imshow('green', holidayGreen)
			#cv.imshow('orange', orange)

			cv.imshow(fileBase, frame)
			#cv.imshow('Frame', v)
			#cv.imshow('Frame', s)
			#cv.imshow('Frame', h)

			# Press Q on keyboard to  exit
			if cv.waitKey(25) & 0xFF == ord('q'):
				break
		else:
			print("Reached the end of the file.")
			break

	except:
		print("There was an exception.  This was probably because it didn't find any blobs.")

# When everything done, release the video capture object
vid.release()

file1.close() 

# Closes all the frames
cv.destroyAllWindows()