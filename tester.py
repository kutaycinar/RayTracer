#    Kutay Cinar V00******    #

import os

# Tests every test file in testing directory
for fname in os.listdir("tests/."):

	if fname.endswith(".txt"):
		print(fname)
		os.system('python3 RayTracer.py tests/' + fname)
