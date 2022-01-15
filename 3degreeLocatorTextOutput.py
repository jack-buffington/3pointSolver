import math

# Now read a bit of the file so I have a reference about how to do it.
# inFile = open("simulation.txt","r")
# outFile = open("simulationSolutions.txt","w")

# inFile = open("circleTriangleSquare600_760.txt","r")
# outFile = open("circleTriangleSquare600_760Solutions.txt","w")


fileBase = input("Please enter the base file name to work on.")
inFileName = fileBase + "_centerAdjusted.txt"
outFileName = fileBase + "_solutions.txt"

print(f"in: {inFileName}")
print(f"out: {outFileName}")


inFile = open(inFileName,"r")
outFile = open(outFileName,"w")


# inFile = open("straightLineWhileChangingDirections670x690.txt","r")
# outFile = open("straightLineWhileChangingDirections670x690_SOLUTION.txt","w")


line = inFile.readline()
print(line)


line = inFile.readline()


lineCount = 2
while line:
#line = inFile.readline()
	# print(f"Working on line {lineCount}")
	# lineCount += 1
	# print(line)
	# split the line into individual numbers.
	splitLine = line.split(',')



	# The distances are already known so let's just stick them in variables
	orangBlueDistance = 2.087
	greenOrangeDistance = 3.176
	redGreenDistance = 2.087
	blueRedDistance = 3.176

	# load one line into some variables
	blueX = float(splitLine[0])
	blueY = float(splitLine[1])
	orangeX = float(splitLine[2])
	orangeY = float(splitLine[3])
	greenX = float(splitLine[4])
	greenY = float(splitLine[5])
	redX = float(splitLine[6])
	redY = float(splitLine[7])

	robotX = float(splitLine[8])	# These three were included so that I could check my work
	robotY = float(splitLine[9])
	robotHeading = float(splitLine[10])


	# print("Measured values:")
	# print(f"Blue: {blueX}, {blueY}")
	# print(f"Orange: {orangeX}, {orangeY}")
	# print(f"Green: {greenX}, {greenY}")
	# print(f"Red: {redX}, {redY}")
	# print(f"Robot: {robotX}, {robotY}, {robotHeading}")

	# These are the actual positions of the landmarks
	actualBlueX = 1.0
	actualBlueY = 3.087
	actualOrangeX = 1.0
	actualOrangeY = 1.0
	actualGreenX = 4.176
	actualGreenY = 1.0


	# Figure out the angles to each of the landmarks
	blueAngle = math.atan2(blueY, blueX)
	orangeAngle = math.atan2(orangeY, orangeX)
	greenAngle = math.atan2(greenY, greenX)
	redAngle = math.atan2(redY, redX)

	# print(f"Angles: blue: {blueAngle}  orange: {orangeAngle}  green: {greenAngle}  red: {redAngle}")


	# Figure out the angles between the landmarks
	orangeBlueAngle = orangeAngle - blueAngle
	greenOrangeAngle = greenAngle - orangeAngle
	redGreenAngle = redAngle - greenAngle
	blueRedAngle = blueAngle - redAngle 


	# print(f"orange to blue angle: {orangeBlueAngle}")
	# print(f"green to orange angle: {greenOrangeAngle}")



	# ###########################
	# #### The first circle #####
	# ###########################
	# Figure out the offset from line segment AB, which has length E 
	# Use the formula E = AB/(2 * tan theta)

	denominator = 2 * math.tan(orangeBlueAngle)
	if denominator != 0:
		distanceE = orangBlueDistance / denominator
	else:
		print("This position would have resulted in a division by zero...")
		line = inFile.readline()
		continue

	#distanceE = orangBlueDistance / denominator
	#Find the midpoint of AB
	deltaX = actualBlueX - actualOrangeX
	deltaY = actualBlueY - actualOrangeY
	midpointX = (deltaX / 2) + actualOrangeX 	# this is in coordinates relative to the observer, not actual.  I should be using actual here.  
	midpointY = (deltaY / 2) + actualOrangeY


	# print(f"First circle - distanceE: {distanceE} ")
	# print(f"midPoint between orange and blue: {midpointX}, {midpointY}")  
	# print(f"deltaX: {deltaX}  deltaY: {deltaY}")							

	# find the perpendicular angle
	angle = math.atan2(-deltaX, deltaY)

	# print(f"perpendicular angle: {angle}")				

	# Use that angle and the distance with sin and cos to find the center location
	center1X = (distanceE * math.cos(angle)) + midpointX
	center1Y = (distanceE * math.sin(angle)) + midpointY

	# print(f"Circle 1's center: {center1X}, {center1Y}\n\n")		# CORRECT TO HERE








	# ############################
	# #### The second circle #####
	# ############################
	# Figure out the offset from line segment AB, which has length E 
	# Use the formula E = AB/(2 * tan theta)

	denominator = 2 * math.tan(greenOrangeAngle)
	if denominator != 0:
		distanceE = greenOrangeDistance / denominator
	else:
		print("This position would have resulted in a division by zero...")
		line = inFile.readline()
		continue
	#Find the midpoint of AB
	deltaX = actualGreenX - actualOrangeX
	deltaY = actualGreenY - actualOrangeY

	# print(f"deltaX: {deltaX}  deltaY: {deltaY}")	

	midpointX = (deltaX / 2) + actualOrangeX 	
	midpointY = (deltaY / 2) + actualOrangeY
	# print(f"midPoint between orange and green: {midpointX}, {midpointY}") 



	# print(f"second circle - distanceE: {distanceE} ")
	 
							

	# find the perpendicular angle
	angle = math.atan2(-deltaX, deltaY)

	# print(f"perpendicular angle: {angle}")				

	# Use that angle and the distance with sin and cos to find the center location
	center2X = (distanceE * math.cos(angle)) + midpointX
	center2Y = -(distanceE * math.sin(angle)) + midpointY			#  ##################### NOTE THAT I HAD TO invert the sign of the offset from the midpoint.   Figure out why...


	# print(f"Circle 2's center: {center2X}, {center2Y}\n\n")


	# Find the slope between the circle centers
	centerSlopeX = center2X - center1X
	centerSlopeY = center2Y - center1Y
	centerSlope = centerSlopeY / centerSlopeX

	# print(f"center slope: {centerSlopeX}, {centerSlopeY},  slope: {centerSlope}")    # #################  Looks good to here.


	perpendicularSlopeX = -centerSlopeY
	perpendicularSlopeY = centerSlopeX
	perpendicularSlope = perpendicularSlopeY / perpendicularSlopeX

	# print(f"perpendicular slope: {perpendicularSlopeX}, {perpendicularSlopeY},  slope: {perpendicularSlope}")		# ############# this looks good 



	# print(f"Slope between circle centers: {centerSlope}")
	# print(f"Perpendicular slope: {perpendicularSlope}")


	# Find the intersection between the line segment between circle centers and the line that passes through B that 
	# is perpendicular to the line segment between the circle centers
	# y = mx + b
	# y0 - y1 = m(x0-x1)

	# I already have both slopes and I have a point for both lines so now calculate the 'b' for each line
	# b = y - mx
	centerB = center1Y - (centerSlope * center1X) 
	midpointB = actualOrangeY - (perpendicularSlope * actualOrangeX)


	# Solve for the X coordinate by setting the two line formulas equal to each other  m1x + b1 = m2x + b2
	# x(m1 - m2) = b2 - b1
	# x = (b2 - b1) / (m1 - m2)
	# 1 is midpoint  2 is center

	intersectionX = (centerB - midpointB) / (perpendicularSlope - centerSlope)

	# Now plug that back into the line formula to get the solution
	intersectionY = centerSlope * (intersectionX - center2X) + center2Y

	#print(f"Intersection between circle centers and line from B to observer: {intersectionX}, {intersectionY}")


	# Find the delta(x,Y) from B to that point then double it to compute the circle's center
	deltaX = intersectionX - actualOrangeX
	deltaY = intersectionY - actualOrangeY

	computedRobotX = (2 * deltaX) + actualOrangeX
	computedRobotY = (2 * deltaY) + actualOrangeY

	#print(f"Computed robot location: {computedRobotX}, {computedRobotY}")





	# Given that I know the actual position of the robot and have the measured position of point A, compute the heading of the robot.
	actualAngleToA = math.atan2(actualBlueY - computedRobotY, actualBlueX - computedRobotX)
	measuredAngleToA = math.atan2(blueY, blueX)

	# print(f"Actual angle: {actualAngleToA}")
	# print(f"Measured angle: {measuredAngleToA}")

	computedRobotHeading = actualAngleToA - measuredAngleToA

	# Keep the angle to the range of 0-2pi
	if computedRobotHeading < 0:
		computedRobotHeading += 6.283185307



	# Check my answers!
	#print(f"\nSanity check:\nActual:   \tX:{robotX}\tY:{robotY}\tHeading:{robotHeading}")
	#print(f"computed: \tX:{computedRobotX}\tY:{computedRobotY}\tHeading:{computedRobotHeading}\n")
	outFile.write(f"{computedRobotX}, {computedRobotY}, {computedRobotHeading}\n")

	line = inFile.readline()

inFile.close()