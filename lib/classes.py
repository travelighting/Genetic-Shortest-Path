import numpy.random as rand
import linechart
import matplotlib.pyplot as plt

plt.style.use('ggplot')

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
            # Check if the distance was already calculated
            if key in distances.keys():
                self.fitness += distances[key]
            # Else calculate it
            else:
                distance = fitnessFunction(lookupTable[self.values[i]],
                                               lookupTable[self.values[i + 1]])
                self.fitness += distance
                # Store the distance
                distances[key] = distance
                
# List of paths
class Population:
    
    def __init__(self, lookupTable):
        size = len(lookupTable.keys())
        self.individuals = [Individual(lookupTable) for _ in range(size)]
        # For dynamic plotting use matplotlib.pyplot.ion()
        plt.ion()
        
    # Sort population according to their fitness
    def sort(self):
        self.individuals = sorted(self.individuals, key=lambda indi: indi.fitness)
                    
    def evaluate(self, fitnessFunction, lookupTable):
        # Objective fitness
        for indi in self.individuals:
            indi.evaluate(fitnessFunction, lookupTable)
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
        fig, = plt.plot([], [])
        # Extract the order of points of the best individual
        for point in self.individuals[0].values:
            x.append(lookupTable[point][0])
            y.append(lookupTable[point][1])
        # Clear the plot
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
