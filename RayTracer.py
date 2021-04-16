#    Kutay Cinar V00******    #

import sys
import numpy as np
from RayTracerFunctions import *
import matplotlib.pyplot as plt

# --------------------------- #
# Parse Command Line Argument #
# --------------------------- #

if len(sys.argv) != 2:
	exit('ERROR: Unexpected input, usage: python3 RayTracer.py <testFile.txt>')

file_name = sys.argv[1]

# --------------------------- #
#    Parse Input Test File    #
# --------------------------- #

NEAR, LEFT, RIGHT, BOTTOM, TOP, RES, SPHERES, LIGHTS, BACK, AMBIENT, OUTPUT = parseTXT(file_name)

# --------------------------- #
#        Main Function        #
# --------------------------- #

# Scene parameters
width, height = RES
eye = np.array([0, 0, 0])

# Output color image
color = np.empty((height, width, 3))

# For every pixel in height
for r in range(height):

	# For every pixel in width
	for c in range(width):

		# Calculate x,y,z vectors as per slides (14)
		x = (RIGHT * ( 2*c / width - 1 ))
		y = (TOP * ( 2*(height-r) / height - 1 ))
		z = (-NEAR)

		# Get direction array and create ray from eye
		direction = np.array([x, y, z])
		ray = (direction + eye)
		color[r, c] = raytrace(eye, ray, SPHERES, LIGHTS, depth=1, max_depth=3, scene_ambient=AMBIENT, background=BACK, near=NEAR)
	
	# Report progress
	progress(r+1, height)

# --------------------------- #
#    Save Output Test File    #
# --------------------------- #

# outputPPM(OUTPUT, width, height, color) # save ppm (assignment requirement)
plt.imsave(OUTPUT[:-3]+'png', color) # save png

# end of file