# check_setup.py - is my computer ready for the robotics course?
import sys
print("Python version:", sys.version.split()[0])

import numpy
print("numpy version:", numpy.__version__)

import matplotlib
print("matplotlib version:", matplotlib.__version__)

print("All good! Your computer is ready.")
