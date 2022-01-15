# 3pointSolver
This repository contains code that allows you to figure out the X/Y location and heading of your robot 
using a camera and three landmarks.

The files in this repository are:
3degreeLocatorTextOutput.py:
	This script loads in a text file ending in "_centerAdjusted.txt" and computes a position and heading, 
	which are saved out to a text file ending in "_solutions.txt"

centerPointAdjuster.py:
	This script loads a text file that contains all of the centroids for the landmarks that were seen which 
	are in image coordinates and subtacts out the location of the optical center of the lens.  The results
	are saved with a suffix of "_centerAdjusted.txt".

dataPlotter.py
	This script plots the positions of the results found by 3degreeLocatorTextOutput.py

findBlobs.py
	This is a very slow script that searches for the largest blob that fits the critera that I have chosen 
	for each of the four colors and outputs their locations in a text file with the same base name as the 
	provided video file. 

findBlobsWithGray.py
	This script is a lot faster than findBlobs.py.  It does the same thing for the first fram but thereafter
	it searches a small area around where each blob was found previously using just the saturation channel 
	as its input.   It performs a lot better because it isn't getting distracted by fringing at the edges.

findCenter.py
	This script allows you to find the optical center of a lens through trial and error using command line 
	arguments.   It does this by drawing a circle over the video as it plays.  You just keep re-running it
	and changing the parameters until things look good.  There is definitely a better solution that would 
	use computer vison techniques but I didn't have time to implement them.   This manual process is the 
  	best that I had time for.  


Note that all of these scripts are in Python.   I don't really recommend implementing this algorithm this way 
since Python is slow and my blob finder could be many times faster if it was made with a compiled language.   
I will probably revisit this algorithm once I get done playing around with lidar on my mapping robot and will 
almost certainly make this more robust and efficient in C++.  My recommendation is that you look at what I 
have done here and then rewrite this in a compiled language.  

I haven't included any video files here but have put the following on my web server:
http://www.robotbrigade.com/random/new_circle.mp4   
http://www.robotbrigade.com/random/new_rectangle.mp4
http://www.robotbrigade.com/random/new_triangle.mp4
