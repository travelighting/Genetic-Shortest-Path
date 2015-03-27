import numpy.random as rand
import numpy as np
import linechart
import matplotlib.pyplot as plt
import sys

# Save the distances to reduce calculations
distances = {}

# Path
class Individual:
    
    def __init__(self, lookupTable):
        # List of points
        self.values = list(lookupTable.keys())
        rand.shuffle(self.values)
        self.fitness = None
        
    def evaluate(self, fitnessFunction, lookupTable):
        self.fitness = 0
        for i in range(len(self.values) - 1):
            key = str(self.values[i]) + '-' + str(self.values[i + 1])
            if key in distances.keys():
                self.fitness += distances[key]
            else:
                distance = fitnessFunction(lookupTable[self.values[i]],
                                               lookupTable[self.values[i + 1]])
                self.fitness += distance
                distances[key] = distance
                

        # Without memoization
##        self.fitness = np.sum((fitnessFunction(lookupTable[self.values[i]],
##                                               lookupTable[self.values[i + 1]])
##                               for i in range(len(self.values) - 1)))

# List of paths
class Population:
    
    def __init__(self, lookupTable):
        size = len(lookupTable.keys())
        self.individuals = [Individual(lookupTable) for _ in range(size)]
        # For dynamic plotting use matplotlib.pyplot.ion()
        plt.ion()
        
    # Sort population according to their fitness
    def sort(self):
        # Bubble sort from worst to best
        sorted = False
        while sorted == False:
            sorted = True
            for i in range(len(self.individuals) - 1):
                indiOne = self.individuals[i]
                indiTwo = self.individuals[i + 1]
                if indiOne.fitness > indiTwo.fitness:
                    self.individuals[i], self.individuals[i + 1] = indiTwo, indiOne
                    sorted = False
                    
    def evaluate(self, fitnessFunction, lookupTable):
        # Objective fitness
        for i in range(len(self.individuals)):
            self.individuals[i].evaluate(fitnessFunction, lookupTable)
        # Sort population
        self.sort()

    def fitnesses(self):
        return [indi.fitness for indi in self.individuals]
    
    def values(self):
        return [indi.values for indi in self.individuals]

    def plot2D(self, lookupTable, generation):
        assert len(lookupTable[self.individuals[0].values[0]]) == 2, 'Data points are not of dimension 2.'
        x = []
        y = []

        '''TO DO'''
        labels = []
        
        fig, = plt.plot([], [])
        # Extract the order of points of the best individual
        for point in self.individuals[0].values:
            x.append(lookupTable[point][0])
            y.append(lookupTable[point][1])
            labels.append(point)
        # Cleer the plot
        plt.clf()
        plt.scatter(x, y, alpha=0.5)
        # Join points
        linechart.colorline(x, y)
        plt.title('Generation : ' + str(generation) + ' / ' +
                  'Best path : ' + str(self.fitnesses()[0]))
        # Necessary for plt.ion()
        plt.pause(5e-324)
        
    def plot3D(self, lookupTable):
        assert len(lookupTable[self.individuals[0]]) == 3, 'Data points are not of dimension 3.'
        
