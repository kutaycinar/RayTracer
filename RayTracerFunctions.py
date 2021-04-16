#    Kutay Cinar V00******    #

import sys
import numpy as np
from numpy import linalg as LA

def parseTXT(fname):
	"""
	Test file TXT parser for testFile.txt format.

	:param fname: name of the file to be parsed
	:return NEAR: start of the near plane
	:return LEFT, RIGHT, TOP, BOTTOM: positions of view boxes
	:return RES: resolution in tuple (width x height)
	:return SPHERES, LIGHTS: list of spheres and lights
	:return BACK, AMBIENT: background color and ambient light (r,g,b)
	:return OUTPUT: output filename
	""" 

	SPHERES = []
	LIGHTS = []
	
	with open(fname) as f:
		lines = f.readlines()
		
		for line in lines:
			words = line.split()

			if len(words) < 2:
				continue

			if words[0] == 'NEAR':
				NEAR = float(words[1])

			if words[0] == 'LEFT':
				LEFT = float(words[1])

			if words[0] == 'RIGHT':
				RIGHT = float(words[1])

			if words[0] == 'BOTTOM':
				BOTTOM = float(words[1])

			if words[0] == 'TOP':
				TOP = float(words[1])

			if words[0] == 'RES':
				RES = (int(words[1]), int(words[2]))

			if words[0] == 'SPHERE':

				if len(words) != 16:
					continue

				sphere = {
					'name': words[1],
					'pos x': float(words[2]),
					'pos y': float(words[3]),
					'pos z': float(words[4]),
					'scl x': float(words[5]),
					'scl y': float(words[6]),
					'scl z': float(words[7]),
					'r': float(words[8]),
					'g': float(words[9]),
					'b': float(words[10]),
					'Ka': float(words[11]),
					'Kd': float(words[12]),
					'Ks': float(words[13]),
					'Kr': float(words[14]),
					'n': float(words[15])
				}

				sphere['pos'] = np.array([sphere['pos x'], sphere['pos y'], sphere['pos z']])
				sphere['scl'] = np.array([sphere['scl x'], sphere['scl y'], sphere['scl z']])
				sphere['rgb'] = np.array([sphere['r'], sphere['g'], sphere['b']])

				sphere['matrix'] = np.array(
				[
					[sphere['scl x'], 0, 0, sphere['pos x']],
					[0, sphere['scl y'], 0, sphere['pos y']],
					[0, 0, sphere['scl z'], sphere['pos z']],
					[0, 0, 0, 1]
				])

				sphere['matrix_inv'] = np.array(
				[
					[1/sphere['scl x'], 0, 0, -sphere['pos x']/sphere['scl x']],
					[0, 1/sphere['scl y'], 0, -sphere['pos y']/sphere['scl y']],
					[0, 0, 1/sphere['scl z'], -sphere['pos z']/sphere['scl z']],
					[0, 0, 0, 1]
				])

				SPHERES.append(sphere)

			if words[0] == 'LIGHT':
				
				if(len(words) != 8):
					continue

				light = {
					'name': words[1],
					'pos x': float(words[2]),
					'pos y': float(words[3]),
					'pos z': float(words[4]),
					'Ir': float(words[5]),
					'Ig': float(words[6]),
					'Ib': float(words[7]),
				}
				
				light['pos'] = np.array([light['pos x'], light['pos y'], light['pos z']])
				light['rgb'] = np.array([light['Ir'], light['Ig'], light['Ib']])

				LIGHTS.append(light)

			if words[0] == 'BACK':
				BACK = (float(words[1]), float(words[2]), float(words[3]))

			if words[0] == 'AMBIENT':
				AMBIENT = (float(words[1]), float(words[2]), float(words[3]))

			if words[0] == 'OUTPUT':
				OUTPUT = words[1]

	try:
		NEAR, LEFT, RIGHT, BOTTOM, TOP, RES, BACK, AMBIENT, OUTPUT
	except:
		exit('ERROR: Bad testing file, has missing parameters.')

	if len(SPHERES) == 0:
		exit('ERROR: Bad testing file, there are no spheres.')
		
	if len(LIGHTS) == 0:
		exit('ERROR: Bad testing file, there are no lights.')

	return NEAR, LEFT, RIGHT, BOTTOM, TOP, RES, SPHERES, LIGHTS, BACK, AMBIENT, OUTPUT

def progress(current, end, length=25):
	"""
	Report the progress in the format: 'RayTracing: [++++++-------------------] 25.2%'
	:param current: current position on loading bar
	:param end: last position on loading bar
	:param: length: loading bar size (default 25)
	""" 
	percent = current / end
	hashes = '+' * int(round(percent * length, 1))
	dashes = '-' * (length - len(hashes))
	sys.stdout.write(f'\rRayTracing: [{hashes + dashes}] {round(percent * 100, 1)}%')
	sys.stdout.flush()
	if percent == 1:
		print('')

def normalize(vector):
	"""
	Normalize function.
	:param vector: a numpy array to be normalized
	:return: normalized vector
	""" 
	return vector / LA.norm(vector)

def sphere_intersect(ray_origin, ray_direction, sphere):
	"""
	Calculate if a ray intersects with a given sphere.
	:param ray_origin: ray origin position
	:param ray_direction: ray direction vector
	:param sphere: the sphere for calculation
	:return: solutions of quadtratic equation (x1,x2) or None for no solution
	""" 

	# Calculate a, b, and c with sphere equation
	a = LA.norm(ray_direction)**2
	b = np.dot(ray_origin, ray_direction)
	c = LA.norm(ray_origin)**2 - 1
	d = b ** 2 - a * c 

	# Discrement >= 0 means two solutions
	if d >= 0:
		x1 = (-b + np.sqrt(d)) / (a)
		x2 = (-b - np.sqrt(d)) / (a)
		return (x1,x2)
	
	# Otherwise no solution
	return None

def closest_intersect(ray_origin, ray_direction, spheres, lights, depth=0, near=0):
	"""
	Calculate the closest intersecting sphere with a ray.
	:param ray_origin: ray origin position
	:param ray_direction: ray direction vector
	:param spheres: list of spheres
	:param lights: list of lights
	:param depth: ray depth (default 0)
	:param near: near plane (default 0)
	:return: closest sphere and the intersection distance or None if it does not exist
	""" 

	# Set result as none and mininimum distance as infinity
	result = None
	min_dist = np.inf

	# For every sphere in scene
	for sphere in spheres:

		# Calculate inverse ray origin and ray direction that includes scale factors)
		ray_origin_inv = np.matmul(sphere['matrix_inv'], np.append(ray_origin, 1))[:3]
		ray_direction_inv = np.matmul(sphere['matrix_inv'], np.append(ray_direction, 0))[:3]

		# Get solutions from the intersection with sphere
		solutions = sphere_intersect(ray_origin_inv, ray_direction_inv, spheres)
		
		if solutions is not None:
			for solution in solutions:
				if solution < min_dist and solution > 1e-6:
					# EDGE CASE: depth 1 must check NEAR plane intersection
					if depth == 1:
						z = np.dot(ray_direction * solution, [0,0,-1])
						if z > 1:
							result = (sphere, solution)
							min_dist = solution
					else:
						result = (sphere, solution)
						min_dist = solution
	return result

def raytrace(ray_origin, ray_direction, spheres, lights, depth, scene_ambient, background, max_depth=3, near=0):
	"""
	A recursive function for tracing rays out of a scene.
	:param ray_origin: ray origin position
	:param ray_direction: ray direction vector
	:param spheres: list of spheres
	:param lights: list of lights
	:param depth: ray depth
	:param scene_ambient: ambient value of scene
	:param background: color of background
	:param max_depth: maximum ray bounce value (default 3)
	:param near: near plane (default 0)
	:return: color value of a pixel
	""" 

	# Recursion base case
	if depth > max_depth:
		return np.zeros(3)

	# Get closest intersection from ray
	intersection = closest_intersect(ray_origin, ray_direction, spheres, lights, depth, near)

	# Return background color if intersection is None
	if intersection is None:
		if depth>1:
			return np.zeros(3)
		else:
			return background

	# Get intersected sphere and distance
	sphere, dist = intersection

	# Ambient Color
	ambient = sphere['rgb'] * sphere['Ka'] * scene_ambient

	# Diffuse and Specular Color
	diffuse = np.zeros(3)
	specular = np.zeros(3)

	# Point of intersection
	P = ray_origin + ray_direction * dist

	# Normal vector
	N = P - sphere['pos']
	N = np.matmul(LA.inv(sphere['matrix'].transpose()), np.matmul(np.append(N, 1), sphere['matrix_inv']))[:3]
	N = normalize(N)
	
	# EDGE CASE: Backface
	if np.dot(ray_direction, N) > 0 and depth == 1:
		# SPECIAL CASE: Check if a light exists within sphere
		for light in lights:
			L = light['pos'] - P
			intersect = closest_intersect(P, L, spheres, lights)
			# Make sure there is an intersect
			if intersect is None:
				continue
			intersect_sphere, intersect_distance = intersect
			# Make sure the ray intersect is with SAME sphere
			if sphere['name'] != intersect_sphere['name']:
				continue
			# Make sure the distance intersected is less than light vector's magnitude
			if np.dot(L, L) >= intersect_distance:
				continue
			# If here, it means the light is inside the sphere's parameters
			R = normalize(2*(np.dot(N, L)) * N - L)
			L = normalize(L)
			V = normalize(-P)
			diffuse = np.add(diffuse, sphere['Kd'] * light['rgb'] * np.dot(L, -N) * sphere['rgb'])
			specular = np.add(specular, sphere['Ks'] * light['rgb'] * np.dot(R, V) ** sphere['n'])
			
		# Return back edge face's colors
		return ambient + diffuse + specular

	if not(sphere['Kd'] == 0.0 and sphere['Ks'] == 0.0):
		# Diffuse and Specular calculation
		for light in lights:
			L = light['pos'] - P
			shadow = closest_intersect(P, L, spheres, lights)
			if shadow is not None:
				continue
			R = normalize(2*(np.dot(N, L)) * N - L)
			L = normalize(L)
			V = normalize(-P)
			diffuse = np.add(diffuse, sphere['Kd'] * light['rgb'] * np.dot(L, N) * sphere['rgb'])
			specular = np.add(specular, sphere['Ks'] * light['rgb'] * np.dot(R, V) ** sphere['n'])

	# Reflection Color
	reflection = np.zeros(3)

	if sphere['Kr'] != 0.0:
		# Reflection calculation at next ray depth
		depth = depth + 1
		ray_reflected = (-2) * np.dot(N, ray_direction) * N + ray_direction
		reflection = sphere['Kr'] * raytrace(P, ray_reflected, spheres, lights, depth, scene_ambient, background, max_depth=max_depth)

	# Return all color information
	return ambient + diffuse + specular + reflection

def outputPPM(filename, width, height, image, maxval=255):
	"""
	Outputs images in .ppm format (P6).
	:param filename: name of the file
	:param width: width of final image
	:param height: height of final image
	:param image: image array to be written to file
	:param maxval: maximum pixel intensity (default 255) 
	""" 
	image = np.clip(image * maxval, 0, maxval)
	ppm_header = f'P6 {width} {height} {maxval}\n'
	with open(filename, 'wb') as f:
		f.write(bytearray(ppm_header, 'ascii'))
		f.write(image.astype('int8').tobytes())

# end of file