import sys, os
projectpath = os.path.dirname(os.path.realpath('classes.py'))
libpath = projectpath + '/lib'
sys.path.append(libpath)
os.chdir(projectpath)
from classes import Population
from mutations import *
import pandas as pd
import distances
from copy import deepcopy

# Create a grid
n = 5
df = pd.DataFrame()
x = []
y = []
for i in range(n):
    for j in range(n):
        x.append(i)
        y.append(j)
df['X'] = x
df['Y'] = y

# Create the lookup table
lookupTable = {}
for i, record in df.iterrows():
    key = i
    lookupTable[key] = (record['X'], record['Y'])

# Parameters
generations = 10000
distance = distances.euclidian 

# Initialize a population
paths = Population(lookupTable)
paths.evaluate(distance, lookupTable)

for g in range(generations):
    # Generate offsprings
    newPaths = []
    for path in paths.individuals[:10]:
        # Create 1 exact copy of each top 10 paths
        newPaths.append(deepcopy(path))
        # Create 3 offsprings with 1 to 3 mutations
        for _ in range(3):
           newPaths.append(mutatePath(deepcopy(path), 3))
        # Create 6 offsprings with a single shuffle of maximal size 10
        for _ in range(6):
            newPaths.append(shufflePath(deepcopy(path), 10))
    # Replace the old population with the new population of offsprings
    paths.individuals = deepcopy(newPaths)
    paths.evaluate(distance, lookupTable)
    paths.plot2D(lookupTable, g)
