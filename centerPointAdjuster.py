# centerPointAdjuster.py
# This program shifts the origin of the image to the location of the optical center of the lens.

opticalX = float(input("What is the X location of the optical center?"))
opticalY = float(input("What is the Y location of the optical center?"))
fileBase = input("What is the base file name? (without without .txt)")

inFileName = fileBase + ".txt"
outFileName = fileBase + "_centerAdjusted.txt"


print (f"You entered {opticalX}, {opticalY}")
print (f"In:  {inFileName}   out: {outFileName}")


inFile = open(inFileName, "r")
outFile = open(outFileName,"w")


outFile.write("blueX, blueY, orangeX, orangeY, greenX, greenY, redX, redY, robotX, robotY, robotAngle\n")
line = inFile.readline() # This is the heading line.  
line = inFile.readline()

while line:
	splitLine = line.split(',')

	# load one line into some variables
	blueX = float(splitLine[0]) - opticalX
	blueY = float(splitLine[1]) - opticalY
	orangeX = float(splitLine[2]) - opticalX
	orangeY = float(splitLine[3]) - opticalY
	greenX = float(splitLine[4]) - opticalX
	greenY = float(splitLine[5]) - opticalY
	redX = float(splitLine[6]) - opticalX
	redY = float(splitLine[7]) - opticalY

	robotX = float(splitLine[8])	# These three were included so that I could check my work
	robotY = float(splitLine[9])
	robotHeading = float(splitLine[10])


	outFile.write(f"{blueX}, {blueY}, {orangeX}, {orangeY}, {greenX}, {greenY}, {redX}, {redY}, 0, 0, 0\n")
	line = inFile.readline()

inFile.close()
outFile.close()
