# final data plotter
# This plots the data created by the 3 landmark locator program so that I can see if it works!

# load the data one by one 


import matplotlib.pyplot as plt
fileBase = input("Please enter the base file name: ")
inFileName = fileBase + "_solutions.txt"

inFile = open(inFileName , "r")


line = inFile.readline()

lineCount  = 1


fig = plt.figure()
ax = plt.axes()
plt.xlim(-1, 6)
plt.ylim(-1, 5)

while line:
	#print(f"Working on line {lineCount}")
	lineCount += 1
	splitLine = line.split(',')
	X = float(splitLine[0])
	Y = 5 - float(splitLine[1])
	heading = float(splitLine[2])
	print(f"{X}\t{Y}")
	plt.plot(X, Y, 'ro')
	line = inFile.readline()

plt.show()