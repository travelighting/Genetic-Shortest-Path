import sys, os
projectpath = os.path.dirname(os.path.realpath('crossings.py'))
libpath = projectpath + '/lib'
sys.path.append(libpath)
os.chdir(projectpath)
import pandas as pd
from classes import Population
from crossings import *
import distances
from copy import deepcopy

continent = 'Europe'

# Create the lookup table
df = pd.read_csv('data/country-capitals.csv')
df = df[df['ContinentName'] == continent]

# Create a lookup table
lookupTable = {}
for i, record in df.iterrows():
    key = str(record['CountryCode']) + '_' + str(record['CapitalName'])
    lookupTable[key] = (record['CapitalLongitude'], record['CapitalLatitude'])

# Parameters
generations = 1000
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
        # Create 6 offsprings with a single shuffle of maximal size 20
        for _ in range(6):
            newPaths.append(shufflePath(deepcopy(path), 20))
    # Replace the old population with the new population of offspring
    paths.individuals = deepcopy(newPaths)
    paths.evaluate(distance, lookupTable)
    #paths.plot2D(lookupTable, g)
