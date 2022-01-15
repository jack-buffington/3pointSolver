import cv2 as cv
#import apriltag
import numpy as np
import sys

print("run this as follows:\npython3 findCenter.py <video's base name> <X> <Y> <diameter>")


print(f"Arguments count: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
    print(f"Argument {i:>6}: {arg}")

baseName = sys.argv[1]
X = int(sys.argv[2])
Y = int(sys.argv[3])
diameter = int(sys.argv[4])


# print("Starting up...")

# baseName = input("Please enter the base file name: ")

videoName = baseName + ".mp4"
vid = cv.VideoCapture(videoName)


# X = int(input("Center X: "))
# Y = int(input("Center Y: "))
# diameter = int(input("Diameter: "))



# Check if camera opened successfully
if (vid.isOpened()== False):
	print("Error opening video stream or file")



while(vid.isOpened()):
	ret, frame = vid.read()

	if ret == True:
		cv.circle(frame, (X, Y), diameter, (0,255,0), 3)
		cv.imshow('Frame', frame)



		# Press Q on keyboard to  exit
		if cv.waitKey(25) & 0xFF == ord('q'):
			break
	else:
		print("Reached the end of the file.")
		break

	 

# When everything done, release the video capture object
vid.release()

 
