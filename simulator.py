
import numpy as np
import random
import math


blue = (1.0,3.087)
orange = (1.0,1.0)
green = (4.176,1.0)
red = (4.176, 3.087)


file1 = open("simulation02.txt","w")


file1.write("blueX, blueY, orangeX, orangeY, greenX, greenY, redX, redY, robotX, robotY, robotAngle\n")

# Step in X & Y to create a simulation of the robot's movement
# for X in np.arange(-1.0, 5.0, 0.25):
# 	for Y in np.arange(-1.0, 4.0, 0.25):
for X in np.arange(-1.0, 5.0, 1):
	for Y in np.arange(-1.0, 4.0, 1):
		#file1.write(f"Test {X},{Y}\n")
		# Write out a file with the locations of the color patches relative to the robot.
		# <blueX> <blueY> <orangeX> <orangeY> <greenX> <greenY> <redX> <redY> <robotX> <robotY> <robot angle>

		# Translate the color patches so that their coordinates are relative to the robot.
		blueX = blue[0] - X
		blueY = blue[1] - Y
		orangeX = orange[0] - X 
		orangeY = orange[1] - Y 
		greenX = green[0] - X 
		greenY = green[1] - Y 
		redX = red[0] - X 
		redY = red[1] - Y 

		# Rotate the points by a random angle
		angle = random.random() * 6.28
		#print(f"angle: {angle}")

		blueAngle = math.atan2(blueY, blueX) - angle
		blueRadius = math.sqrt(blueX * blueX + blueY * blueY)
		blueX = blueRadius * math.cos(blueAngle)
		blueY = blueRadius * math.sin(blueAngle) 

		orangeAngle = math.atan2(orangeY, orangeX) - angle
		orangeRadius = math.sqrt(orangeX * orangeX + orangeY * orangeY)
		orangeX = orangeRadius * math.cos(orangeAngle)
		orangeY = orangeRadius * math.sin(orangeAngle) 

		greenAngle = math.atan2(greenY, greenX) - angle
		greenRadius = math.sqrt(greenX * greenX + greenY * greenY)
		greenX = greenRadius * math.cos(greenAngle)
		greenY = greenRadius * math.sin(greenAngle) 

		redAngle = math.atan2(redY, redX) - angle
		redRadius = math.sqrt(redX * redX + redY * redY)
		redX = redRadius * math.cos(redAngle)
		redY = redRadius * math.sin(redAngle) 


		file1.write(f"{blueX}, {blueY}, {orangeX}, {orangeY}, {greenX}, {greenY}, {redX}, {redY}, {X}, {Y}, {angle}\n")


file1.close()


# Now read a bit of the file so I have a reference about how to do it.
file1 = open("simulation.txt","r")
line = file1.readline()
print(line)

line = file1.readline()
print(line)
print(" \n")
#split the line into individual numbers.
splitLine = line.split(',')
print(splitLine[0])
print(float(splitLine[0]))



