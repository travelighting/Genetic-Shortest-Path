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
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

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
    # Go through top 10 paths
    for path in paths.individuals[:10]:
        # Create 1 exact copy of each top 10 paths
        newPaths.append(deepcopy(path))
        # Create 3 offsprings with 1 to 3 mutations
        for _ in range(3):
           newPaths.append(mutatePath(deepcopy(path), 3))
        # Create 6 offsprings with a single shuffle of maximal size 20
        for _ in range(6):
            newPaths.append(shufflePath(deepcopy(path), 20))
    # Replace the old population with the new population of offsprings
    paths.individuals = deepcopy(newPaths)
    paths.evaluate(distance, lookupTable)
    #paths.plot2D(lookupTable, g)

# Map the points
bestPath = paths.individuals[0].values
lat = [lookupTable[point][0] for point in bestPath] 
lon = [lookupTable[point][1] for point in bestPath]

map = Basemap(projection='ortho', lat_0 = max(lat)-10, lon_0 = min(lon)-10)
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='lightblue')
map.drawmapboundary() 
x, y = map(lat, lon)
map.plot(x, y, 'ro', markersize=6)
map.plot(x, y, c='red')
##plt.show()
